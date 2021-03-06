import json
import time
import logging
from itertools import chain
from canvasapi.course import Course
from canvasapi.assignment import Assignment
from pymstodo import ToDoConnection
from src.canvas_connect import connect_to_canvas
from src.mstodo_connect import connect_to_ms_todo


def get_courses_to_sync(path="./conf/canvas_to_ms_todo_settings.json") -> dict:
    with open(path, "r", encoding="UTF-8") as file:
        settings = json.load(file)
    courses_to_sync = settings["CoursesToSync"]  # TODO modelify
    logging.info(f"settings successfully read from {path}")
    return courses_to_sync


def get_canvas_assignments(courses: list[Course]) -> list[Assignment]:
    """ Returns a paginated list of assignments. 
        You must iterate over it to get the assignments."""
    # To handle a single course OR a list of courses
    if type(courses) is not list:
        courses = list(courses)
    paginated_course_assignments = [
        course.get_assignments() for course in courses]
    all_assignments = []
    for course_assignments in paginated_course_assignments:
        all_assignments.extend(iter(course_assignments))
    logging.info(f"Got {len(all_assignments)} assignments from canvas.")
    return all_assignments


def make_course_task_list(todo_client: ToDoConnection, courses: list[Course]):
    """ Creates a task list for every course. 
        If the task list already exists it does nothing """
    task_lists = todo_client.get_lists()
    task_list_names = [task_list.displayName for task_list in task_lists]
    # Check if list was created
    modified = False
    for course in courses:
        if course.name not in task_list_names:
            todo_client.create_list(course.name)
            logging.info(f"Created new list {course.name} in MS To-Do.")
            modified = True
        logging.info(f"Task list for course {course.name} already exists.")
    # Update Task List before returning
    if modified:
        logging.debug("Task list was modified.")
        task_lists = todo_client.get_lists()
    return task_lists


def make_course_id_to_list_id_dict(course_dict, task_lists) -> dict:
    """ Maps canvas course ids to MS To-Do list ids """
    course_id_to_list_id_dict = {}
    for course_name, course_id in course_dict.items():
        for task_list in task_lists:
            if course_name.lower() == task_list.displayName.lower():
                course_id_to_list_id_dict[course_id] = task_list.list_id
                logging.debug(
                    f"Mapping course id '{course_id}' to list id '{task_list.list_id}'")
    return course_id_to_list_id_dict


def get_all_task_titles(todo_client: ToDoConnection,
                        course_id_to_list_id_dict: dict) -> list[str]:
    """ The titles are used to determine if the assignment has already been synced to MS To-Do"""
    # Get tasks from task lists associated with a canvas course.
    all_tasks = [todo_client.get_tasks(
        list_id, status="all") for list_id in course_id_to_list_id_dict.values()]
    # Use chain to flatten the list and grab the task titles only
    all_task_titles = [task.title.lower() for task in list(chain(*all_tasks))]
    return all_task_titles


def sync_assignments_to_ms_todo(todo_client: ToDoConnection,
                                assignments: list[Assignment],
                                course_id_to_list_id_dict: dict):
    all_task_titles = get_all_task_titles(
        todo_client,
        course_id_to_list_id_dict)
    for assignment in assignments:
        # Skip if already in ms todo
        if assignment.name.lower() in all_task_titles:
            logging.info(
                f"Skipping assignment '{assignment.name}'. Already in MS To-Do")
            continue
        # If assignment doesn't have a due date; Set it to None
        due_date = None if assignment.due_at is None else assignment.due_at_date
        todo_client.create_task(title=assignment.name,
                                list_id=course_id_to_list_id_dict[assignment.course_id],
                                due_date=due_date,
                                body_text=assignment.html_url)
        logging.info(f"Task '{assignment.name} created.'")


def main():
    canvas_client = connect_to_canvas()
    course_dict = get_courses_to_sync()
    # Get course name to course id dict
    courses = [canvas_client.get_course(id)
               for name, id in course_dict.items()]
    # All assignments for courses in the list
    canvas_assignments = get_canvas_assignments(courses)
    # Establish connection to MS Graph API
    todo_client = connect_to_ms_todo()
    # Create task lists if it does not already exist
    task_lists = make_course_task_list(todo_client, courses)
    course_id_to_list_id_dict = make_course_id_to_list_id_dict(course_dict,
                                                               task_lists)
    while True:
        sync_assignments_to_ms_todo(todo_client,
                                    canvas_assignments,
                                    course_id_to_list_id_dict)
        SLEEPSECONDS = 900
        logging.info(f"Sleeping for {SLEEPSECONDS} seconds.")
        time.sleep(SLEEPSECONDS)


if __name__ == "__main__":
    logging.basicConfig(filename="./data/canvas_to_ms_todo.log",
                        filemode="a",
                        encoding="UTF-8",
                        level=logging.INFO)
    main()
