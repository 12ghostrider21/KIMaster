from pytest import fixture

@fixture
def create_lobby_msg():
    msg = {
        "command": "lobby",
        "command_key": "create" 
    }
    return msg

@fixture
def web_socket_uri():
    return "ws://swtp-server:8000/ws"

@fixture
def max_response_time():
    return 3.0

@fixture
def join_lobby_msg():
    msg = {
        "command":"lobby",
        "command_key":"join",
        "key":""
    }
    return msg