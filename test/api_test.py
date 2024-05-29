import asyncio
import pytest
import logging
import json
from websockets.sync.client import connect
from threading import Event
from api_fixtures import max_response_time, web_socket_uri, create_lobby_msg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_websocket_connection(web_socket_uri):
    '''Checks if a workin connection could be established at all'''
    logging.info("Connecting to swtp-server")
    with connect(web_socket_uri) as conn:
        logging.info("Successful connected to swtp-server")
        pong_event:Event = conn.ping("healthcheck")
        pong_event.wait()
        assert pong_event.is_set()

def test_websocket_connection_ping(web_socket_uri, max_response_time):
    '''Checks if a workin connection could be established and ping is within tolarable time'''
    logging.info("Connecting to swtp-server")
    with connect(web_socket_uri) as conn:
        logging.info("Successful connected to swtp-server")
        pong_event:Event = conn.ping("healthcheck")
        pong_event.wait(max_response_time)
        assert pong_event.is_set()

@pytest.mark.asyncio
async def test_lobby_creation(web_socket_uri, create_lobby_msg):
    logging.info("Connecting to swtp-server")
    with connect(web_socket_uri) as conn:
        logging.info("Successful connected to swtp-server")
        logging.info("Sending create lobby message")
        conn.send(create_lobby_msg)
        message = conn.recv()
        message_as_dict = json.loads(message)
        assert message_as_dict["response_code"] == 100

