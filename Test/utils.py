from websockets.client import ClientConnection
from json import dumps, loads

def to_json(msg:dict) -> str :
    '''type safe conversion of a dict to a json-string'''
    return dumps(msg)

def from_json(json_string:str) -> dict :
    '''type safe conversion of a json-string into a dict'''
    return loads(json_string)

async def send(msg:dict, conn: ClientConnection) -> dict:
    await conn.send(to_json(msg))
    return from_json(await conn.recv())