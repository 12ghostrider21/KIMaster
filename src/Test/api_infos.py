from pytest import fixture
from os import getenv

@fixture
def ws_server_uri():
    scheme:str = getenv('WS_SCHEME', 'ws')
    host:str = getenv('WS_CONTAINER', 'swtp-server')
    port:str = getenv('WS_PORT', '')