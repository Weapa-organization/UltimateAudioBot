from asyncio.log import logger
import requests
from ConectApi.config import *

DEFAULT_STATE = "reverse"

def create_user(user_id, username, state=DEFAULT_STATE):
    r = requests.request("POST", URL_API, json={"user_id": user_id, "username": username, "state": state})
    # r = requests.post(URL_API, data={"user_id": user_id, "username": username, "state": state})
    return state


def get_state(user_id, username):
    r = requests.get(URL_API + USER_BY_ID + str(user_id))
    if r.status_code == 200:
        return r.json()["state"]
    else:
        # crear usuario
        return create_user(user_id, username)


def update_state(user_id, username, state):
    r = requests.put(URL_API + STATE_USER_BY_ID + str(user_id), params={"state": state})
    # logger.info(r.status_code)
    if r.status_code != 200:
        create_user(user_id, username, state)
