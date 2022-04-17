
import json


def generate_settings():
    canvas_settings = {
        "API_URL": "https://yourcanvassite.example",
        "API_KEY": "YOURAPIKEY",
    }

    ms_todo_settings = {
        "CLIENT_ID": "YOURCLIENTID",
        "CLIENT_SECRET": "YOURAPPSECRET",
    }

    canvas_to_ms_todo_settings = {
        "CoursesToSync": {
            "Programming 101": 1234,
            "Discrete Mathematics": 4321,
            "Systems design": 5555
        }
    }
    settings_map = {
        "./canvas_settings.json": canvas_settings,
        "./ms_todo_settings.json": ms_todo_settings,
        "./canvas_to_ms_todo_settings.json": canvas_to_ms_todo_settings
    }
    for path, settings in settings_map.items():
        with open(path, "w") as file:
            json.dump(settings, file, indent=4)


if __name__ == "__main__":
    generate_settings()
    print("Files have been generated and placed in current working directory.")
    print("Modify them with your settings and place them in the conf dir to use them.")
