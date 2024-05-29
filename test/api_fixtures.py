from pytest import fixture
from json import dumps as to_json
from websockets.sync.client import connect
from threading import Event

@fixture
def create_lobby_msg():
    msg = {
        "command": "lobby",
        "command_key": "create" 
    }
    return to_json(msg)

@fixture
def web_socket_uri():
    return "ws://swtp-server:8000/ws"

@fixture
def max_response_time():
    return 3.0