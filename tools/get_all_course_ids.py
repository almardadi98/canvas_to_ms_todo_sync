import json
from canvasapi import Canvas


def write_course_info_to_file(canvas: Canvas) -> None:
    """ You can use this function to write all the courses to the json file. 
        Useful for finding the course ids"""
    courses = canvas.get_courses()

    courses_dict = {course.name: course.id for course in courses}
    with open("./data/courses.json", "w", encoding="UTF-8") as outfile:
        json.dump(courses_dict, outfile, ensure_ascii=False, indent=4)
