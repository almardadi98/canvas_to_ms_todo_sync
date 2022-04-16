import json
from pymstodo import ToDoConnection
from models.ms_todo_settings import MSTODOSettings
import pickle

with open("./conf/ms_todo_settings.json", "r", encoding="UTF-8") as mstodo_file:
    mstodo_settings = MSTODOSettings(**json.load(mstodo_file))

client_id = mstodo_settings.CLIENT_ID
client_secret = mstodo_settings.CLIENT_SECRET


def connect_to_ms_todo() -> ToDoConnection:
    try:
        with open("./data/token.dat", "rb") as file:
            token = pickle.load(file)
    except FileNotFoundError:
        auth_url = ToDoConnection.get_auth_url(client_id)
        redirect_resp = input(
            f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
        token = ToDoConnection.get_token(
            client_id, client_secret, redirect_resp)
        with open("./data/token.dat", "wb") as file:
            pickle.dump(token, file)

    todo_client = ToDoConnection(
        client_id=client_id, client_secret=client_secret, token=token)
    return todo_client
