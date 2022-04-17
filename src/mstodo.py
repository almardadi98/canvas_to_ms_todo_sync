import json
import pickle
from pymstodo import ToDoConnection
from models.ms_todo_settings import MSTODOSettings


def get_ms_todo_settings() -> MSTODOSettings:
    with open("./conf/ms_todo_settings.json", "r", encoding="UTF-8") as mstodo_file:
        mstodo_settings = MSTODOSettings(**json.load(mstodo_file))
    return mstodo_settings


def connect_to_ms_todo() -> ToDoConnection:
    mstodo_settings = get_ms_todo_settings()
    # Load the auth token from file
    try:
        with open("./data/token.dat", "rb") as file:
            token = pickle.load(file)
    except FileNotFoundError:
        # Token does not exist. Proceed to get a new token
        auth_url = ToDoConnection.get_auth_url(mstodo_settings.CLIENT_ID)
        redirect_resp = input(
            f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
        token = ToDoConnection.get_token(
            mstodo_settings.CLIENT_ID, mstodo_settings.CLIENT_SECRET, redirect_resp)
        # Write the token to disk
        with open("./data/token.dat", "wb") as file:
            pickle.dump(token, file)

    todo_client = ToDoConnection(
        client_id=mstodo_settings.CLIENT_ID, client_secret=mstodo_settings.CLIENT_SECRET, token=token)
    return todo_client
