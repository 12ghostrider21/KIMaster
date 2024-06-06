from pytest import fixture

@fixture(autouse=True)
def create_lobby_msg() -> dict:
    return {
        "command": "lobby",
        "command_key": "create" 
    }

@fixture(autouse=True)
def web_socket_uri() -> str:
    return "ws://swtp-server:8000/ws"

@fixture(autouse=True)
def max_response_time() -> float:
    return 3.0

@fixture(autouse=True)
def join_lobby_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"join",
        "key":""
    }

@fixture(autouse=True)
def leave_lobby_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"leave"
    }