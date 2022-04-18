import json
import logging
from canvasapi import Canvas
from models.canvas_settings import CanvasSettings


def connect_to_canvas(path="./conf/canvas_settings.json") -> Canvas:
    """ Connect to canvas using the url and api key specified in the settings"""
    with open(path, "r", encoding="UTF-8") as canvas_file:
        canvas_settings = CanvasSettings(**json.load(canvas_file))
    # Canvas API URL
    API_URL = canvas_settings.API_URL
    # Canvas API key
    API_KEY = canvas_settings.API_KEY
    logging.info(f"settings successfully read from {path}")

    # Initialize a new Canvas object
    canvas_client = Canvas(API_URL, API_KEY)
    return canvas_client
