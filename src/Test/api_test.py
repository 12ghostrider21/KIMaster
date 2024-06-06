import pytest
from json import dumps, loads
from websockets.client import connect, ClientConnection
from threading import Event
from api_fixtures import *

def to_json(msg:dict) -> str :
    '''type safe conversion of a dict to a json-string'''
    return dumps(msg)

def from_json(json_string:str) -> dict :
    '''type safe conversion of a json-string into a dict'''
    return loads(json_string)

async def send(msg:dict, conn: ClientConnection) -> dict:
    await conn.send(to_json(msg))
    return from_json(await conn.recv())


@pytest.mark.asyncio
async def test_websocket_connection(web_socket_uri, max_response_time):
    '''Checks if a workin connection could be established at all'''
    async with connect(web_socket_uri) as conn:
        pong_waiter = await conn.ping("healthcheck")
        latency = await pong_waiter
        assert latency <= max_response_time



@pytest.mark.asyncio
async def test_lobby_creation(web_socket_uri, create_lobby_msg):
    async with connect(web_socket_uri) as conn:
        # create lobby
        res = await send(create_lobby_msg, conn)

        # the response should have a response_code as specified in commands_and_command_keys 
        assert "response_code" in res
        
        # when lobby creation was successful response_code should be 100 as specified in commands_and_command_keys
        assert res["response_code"] == 100

        # the response should have a freshly created lobby key as specified in commands_and_command_keys
        assert "key" in res
        assert res["key"] is not None

        
@pytest.mark.asyncio
async def test_joining_existing_lobby(web_socket_uri, create_lobby_msg, join_lobby_msg):
    # connect as player-1 to the server
    async with connect(web_socket_uri) as conn_player_one:
        # create lobby
        res_one = await send(create_lobby_msg, conn_player_one)

        # get the key of the created lobby
        lobby_key = res_one["key"]

        # second connection to the server
        async with connect(web_socket_uri) as conn_player_two:

            # join the lobby of player 1
            join_lobby_msg["key"] = lobby_key
            res_two = await send(join_lobby_msg, conn_player_two)

            # check if both players are in the same lobby
            assert res_two["key"] == lobby_key

            # check if the response_code meets the specification in commands_and_command_keys
            assert "response_code" in res_two
            assert res_two["response_code"] == 101

@pytest.mark.asyncio
async def test_joining_non_existing_lobby(web_socket_uri, join_lobby_msg):
    async with connect(web_socket_uri) as conn: 
        # try to join a non existing lobby
        join_lobby_msg["key"] = "this_is_only_a_dummy_key_not_a_real_one_therefore_this_key_should_not_be_working"
        res = await send(join_lobby_msg, conn)

        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res
        assert res["response_code"] == 151

@pytest.mark.asyncio
async def test_creating_multiple_lobbies(web_socket_uri, create_lobby_msg):
    # connect as player-1 to the server
    async with connect(web_socket_uri) as conn:
        # create first lobby
        await send(create_lobby_msg, conn)
        
        # no need to run tests on the first lobby, since this is covered in test_lobby_creation()


        # create second lobby
        res = await send(create_lobby_msg, conn)
        
        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res
        assert res["response_code"] == 150

@pytest.mark.asyncio
async def test_joining_multiple_lobbies(web_socket_uri, create_lobby_msg, join_lobby_msg):
    # connect as player-1 to the server
    async with connect(web_socket_uri) as conn_player_one:
        # create lobby
        res_create_lobby = await send(create_lobby_msg, conn_player_one)

        # get the key of the created lobby
        lobby_key = res_create_lobby["key"]

        #connect as player-2 to the server
        async with connect(web_socket_uri) as conn_player_two:

            # first time joining the lobby
            join_lobby_msg["key"] = lobby_key
            res_first_join = await send(join_lobby_msg, conn_player_two)

            # check if both players are in the same lobby
            assert res_first_join["key"] == lobby_key

            # second time joining the lobby
            res_second_join = await send(join_lobby_msg, conn_player_two)

            # check if the response_code meets the specification in commands_and_command_keys 
            assert "response_code" in res_second_join
            assert res_second_join["response_code"] == 150


@pytest.mark.asyncio
async def test_leaving_current_lobby(web_socket_uri, create_lobby_msg, leave_lobby_msg):
    # connect to server
    async with connect(web_socket_uri) as conn:
        # create lobby
        res_create = await send(create_lobby_msg, conn)

        # ensure lobby creation was successful: code 100 is specified in commands_and_command_keys
        assert res_create["response_code"] == 100
        
        # leave lobby
        res_first_leave = await send(leave_lobby_msg, conn)

        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res_first_leave
        assert res_first_leave["response_code"] == 102

        # try to leave the lobby a second time - this should not work since we already left the lobby
        res_second_leave = await send(leave_lobby_msg, conn)
        assert "response_code" in res_second_leave
        assert res_second_leave["response_code"] == 153


@pytest.mark.asyncio
async def test_leaving_non_existing_lobby(web_socket_uri, leave_lobby_msg):
    # connect to server
    async with connect(web_socket_uri) as conn:        
        # leave lobby
        res_leave = await send(leave_lobby_msg, conn)

        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res_leave
        assert res_leave["response_code"] == 153

