import pytest
from time import time
from websockets.client import connect, ClientConnection
from api_lobby_fixtures import *
from utils import send


@pytest.mark.asyncio
async def test_websocket_connection(web_socket_uri: str, max_response_time: float):
    '''Checks if a workin connection could be established at all'''
    async for conn in connect(web_socket_uri):
        try:
            pong_waiter = await conn.ping("healthcheck")
            latency = await pong_waiter
            assert latency <= max_response_time
            await conn.close()
            break
        except ConnectionRefusedError as e:
            continue
        

@pytest.mark.asyncio
async def test_lobby_creation(web_socket_uri: str, create_lobby_msg: dict):
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
async def test_joining_existing_lobby(web_socket_uri: str, create_lobby_msg: dict, join_lobby_msg: dict):
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
            print(res_two)

            # check if both players are in the same lobby
            # assert res_two["key"] == lobby_key

            # check if the response_code meets the specification in commands_and_command_keys
            assert "response_code" in res_two
            assert res_two["response_code"] == 101


@pytest.mark.asyncio
async def test_joining_non_existing_lobby(web_socket_uri: str, join_lobby_msg: dict):
    async with connect(web_socket_uri) as conn: 
        # try to join a non existing lobby
        join_lobby_msg["key"] = "this_is_only_a_dummy_key_not_a_real_one_therefore_this_key_should_not_be_working"
        res = await send(join_lobby_msg, conn)

        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res
        assert res["response_code"] == 151


@pytest.mark.asyncio
async def test_creating_multiple_lobbies(web_socket_uri: str, create_lobby_msg: dict):
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
async def test_joining_multiple_lobbies(web_socket_uri: str, create_lobby_msg: dict, join_lobby_msg: dict):
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
            # assert res_first_join["key"] == lobby_key

            # second time joining the lobby
            res_second_join = await send(join_lobby_msg, conn_player_two)

            # check if the response_code meets the specification in commands_and_command_keys 
            assert "response_code" in res_second_join
            assert res_second_join["response_code"] == 150



# TODO: Test for response_code 152

@pytest.mark.asyncio
async def test_leaving_current_lobby(web_socket_uri: str, create_lobby_msg: dict, leave_lobby_msg: dict):
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
async def test_leaving_non_existing_lobby(web_socket_uri: str, leave_lobby_msg: dict):
    # connect to server
    async with connect(web_socket_uri) as conn:        
        # leave lobby
        res_leave = await send(leave_lobby_msg, conn)

        # check if the response_code meets the specification in commands_and_command_keys 
        assert "response_code" in res_leave
        assert res_leave["response_code"] == 153

@pytest.mark.asyncio
async def test_swap_player(web_socket_uri: str, create_lobby_msg: dict, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    await send(create_lobby_msg, conn_p1)
    
    # swap from player 1 to player 2 (only possible when only one player is in the lobby)
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["pos"] == swap_msg["pos"]
    assert res_swap["response_code"] == 103

    await conn_p1.close()


@pytest.mark.asyncio
async def test_swap_player_when_occupied(web_socket_uri: str, create_lobby_msg: dict, join_lobby_msg: dict, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    conn_p2: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # p2 joins lobby
    join_lobby_msg["key"] = res_create["key"]
    join_lobby_msg["pos"] = "p2"
    await send(join_lobby_msg, conn_p2)
    # p2 sends a broadcast that it joined (101), p1 must remove it from his queue to read the following responses
    await conn_p1.recv()
    
    # swap from player 1 to player 2
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["pos"] == swap_msg["pos"]
    assert res_swap["response_code"] == 155

    await conn_p1.close()
    await conn_p2.close()


@pytest.mark.asyncio
async def test_swap_player_while_not_in_lobby(web_socket_uri: str, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    
    # p1 tries to swap but is not in a lobby
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["response_code"] == 153

    await conn_p1.close()


@pytest.mark.asyncio
async def test_swap_player_to_undefined_pos(web_socket_uri: str, create_lobby_msg: dict, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # try to swap to a undefined position
    swap_msg.pop("pos")    # remove position to make sure it will be unknown
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["response_code"] == 154

    await conn_p1.close()


@pytest.mark.asyncio
async def test_swap_player_to_non_sense_pos(web_socket_uri: str, create_lobby_msg: dict, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # try to swap to a non-sense position
    swap_msg.update({"pos":"jkölhgj,k"})   # change pos argument to non-sense value
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["response_code"] == 154
    assert res_swap["pos"] == swap_msg["pos"]

    await conn_p1.close()


@pytest.mark.asyncio
async def test_swap_player_to_none_pos(web_socket_uri: str, create_lobby_msg: dict, swap_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # try to swap to a None position
    swap_msg.update({"pos":None})   # change pos argument to non-sense value
    res_swap = await send(swap_msg, conn_p1)
    assert res_swap["response_code"] == 154
    assert res_swap["pos"] == swap_msg["pos"]

    await conn_p1.close()


@pytest.mark.asyncio
async def test_get_pos_of_lobby_creator(web_socket_uri: str, create_lobby_msg: dict, pos_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)

    # create lobby
    res_create = await send(create_lobby_msg, conn_p1)

    # test pos of creator
    res_pos_p1 = await send(pos_msg, conn_p1)
    assert res_pos_p1["response_code"] == 104
    assert res_pos_p1["pos"] == "p1"    # p1 is the default for the creator of the lobby

    await conn_p1.close()


@pytest.mark.asyncio
async def test_get_pos_of_p2(web_socket_uri: str, create_lobby_msg: dict, pos_msg: dict, join_lobby_as_p2_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    conn_p2: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # p2 joins lobby
    join_lobby_as_p2_msg["key"] = res_create["key"]
    await send(join_lobby_as_p2_msg, conn_p2)
    
    # test pos of p2
    res_pos_p2 = await send(pos_msg, conn_p2)
    assert res_pos_p2["response_code"] == 104
    assert res_pos_p2["pos"] == "p2"    # p2 is the position of the second player
    
    await conn_p1.close()
    await conn_p2.close()


@pytest.mark.asyncio
async def test_get_pos_of_sp(web_socket_uri: str, create_lobby_msg: dict, pos_msg: dict, join_lobby_as_sp_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    conn_sp: ClientConnection = await connect(web_socket_uri)

    # p1 creates lobby
    res_create = await send(create_lobby_msg, conn_p1)
    
    # sp joins lobby
    join_lobby_as_sp_msg["key"] = res_create["key"]
    await send(join_lobby_as_sp_msg, conn_sp)
    
    # test pos of 2p
    res_pos_sp = await send(pos_msg, conn_sp)
    assert res_pos_sp["response_code"] == 104
    assert res_pos_sp["pos"] == "sp"    # sp2 is the default for all spectators
    
    await conn_p1.close()
    await conn_sp.close()


@pytest.mark.asyncio
async def test_get_pos_with_no_lobby(web_socket_uri: str, pos_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    
    # test pos of p1
    res_pos_sp = await send(pos_msg, conn_p1)
    assert res_pos_sp["response_code"] == 153
    
    await conn_p1.close()


@pytest.mark.asyncio
async def test_lobby_status(web_socket_uri: str, create_lobby_msg: dict, lobby_status_msg: dict, join_lobby_as_p2_msg: dict, join_lobby_as_sp_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    conn_p2: ClientConnection = await connect(web_socket_uri)
    conn_sp1: ClientConnection = await connect(web_socket_uri)
    conn_sp2: ClientConnection = await connect(web_socket_uri)
    
    # test no lobby
    no_lobby_res = await send(lobby_status_msg, conn_p1)
    assert no_lobby_res["response_code"] == 153

    # create lobby
    create_res = await send(create_lobby_msg, conn_p1)

    # test start-up-time is lower than 1 sec
    time_of_creation:float = time()
    res_status_create = await send(lobby_status_msg, conn_p1)
    
    while res_status_create["GameClient"] == False:
        assert time()-time_of_creation <= 1.0
        res_status_create = await send(lobby_status_msg, conn_p1)
    

    # test status after creation
    assert res_status_create["response_code"] == 105
    assert res_status_create["P1"] == True
    assert res_status_create["P2"] == False
    assert res_status_create["Spectators"] == 0
    assert res_status_create["key"] == create_res["key"]
    
    # set up join messages
    join_lobby_as_sp_msg["key"] = create_res["key"]
    join_lobby_as_p2_msg["key"] = create_res["key"]

    # test status after Spectator 1 joined
    await send(join_lobby_as_sp_msg, conn_sp1)
    res_status_sp1 = await send(lobby_status_msg, conn_sp1)
    assert res_status_sp1["response_code"] == 105
    assert res_status_sp1["P1"] == True
    assert res_status_sp1["P2"] == False
    assert res_status_sp1["Spectators"] == 1
    assert res_status_sp1["key"] == create_res["key"]

    # test status after p2 joined
    await send(join_lobby_as_p2_msg, conn_p2)
    res_status_p2 = await send(lobby_status_msg, conn_p2)
    assert res_status_p2["response_code"] == 105
    assert res_status_p2["P1"] == True
    assert res_status_p2["P2"] == True
    assert res_status_p2["Spectators"] == 1
    assert res_status_p2["key"] == create_res["key"]

    # test status after Spectator 2 joined
    await send(join_lobby_as_sp_msg, conn_sp2)
    res_status_sp2 = await send(lobby_status_msg, conn_sp2)
    assert res_status_sp2["response_code"] == 105
    assert res_status_sp2["P1"]
    assert res_status_sp2["P2"]
    assert res_status_sp2["Spectators"] == 2
    assert res_status_sp2["key"] == create_res["key"]

    # close connections
    await conn_p1.close()
    await conn_p2.close()
    await conn_sp1.close()
    await conn_sp2.close()


@pytest.mark.asyncio
async def test_none_lobby_command_key(web_socket_uri: str, empty_lobby_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    
    res = await send(empty_lobby_msg, conn_p1)
    assert res["response_code"] == 52

    await conn_p1.close()


@pytest.mark.asyncio
async def test_non_sense_lobby_command_key(web_socket_uri: str, empty_lobby_msg: dict):
    # connect to server
    conn_p1: ClientConnection = await connect(web_socket_uri)
    
    empty_lobby_msg.update({"command_key":"This_is_useless_command_key_which_should_not_work"})
    res = await send(empty_lobby_msg, conn_p1)
    assert res["response_code"] == 52

    await conn_p1.close()