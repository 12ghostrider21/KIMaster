from pytest import fixture

@fixture
def empty_lobby_msg() -> dict:
    return {
        "command": "lobby",
        "command_key": None 
    }

@fixture
def create_lobby_msg() -> dict:
    return {
        "command": "lobby",
        "command_key": "create" 
    }

@fixture
def web_socket_uri() -> str:
    return "ws://swtp-server:8000/ws"

@fixture
def max_response_time() -> float:
    return 3.0

@fixture
def join_lobby_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"join",
        "key":""
    }

@fixture
def join_lobby_as_p1_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"join",
        "key":"",
        "pos":"p1"
    }

@fixture
def join_lobby_as_p2_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"join",
        "key":"",
        "pos":"p2"
    }

@fixture
def join_lobby_as_sp_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"join",
        "key":"",
        "pos":"sp"
    }

@fixture
def leave_lobby_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"leave"
        }

@fixture
def swap_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"swap",
        "pos":"p2"
    }

@fixture
def pos_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"pos"
    }

@fixture
def lobby_status_msg() -> dict:
    return {
        "command":"lobby",
        "command_key":"status"
    }