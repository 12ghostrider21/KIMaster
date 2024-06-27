from websockets.client import ClientConnection
from json import dumps, loads


# Convert a dictionary to a JSON string
# This function takes a dictionary as input and returns its JSON string representation.
# It ensures that the conversion is type-safe by using the `dumps` method from the `json` module.
def to_json(msg: dict) -> str:
    """type safe conversion of a dict to a json-string"""
    return dumps(msg)


# Convert a JSON string to a dictionary
# This function takes a JSON string as input and returns its dictionary representation.
# It ensures that the conversion is type-safe by using the `loads` method from the `json` module.
def from_json(json_string: str) -> dict:
    """type safe conversion of a json-string into a dict"""
    return loads(json_string)


# Send a dictionary message over a WebSocket connection and receive a response
# This asynchronous function sends a message (in dictionary form) over a WebSocket connection
# and waits for a response. The message is first converted to a JSON string using `to_json`,
# then sent over the WebSocket connection using the `send` method of the connection object.
# After sending, it waits to receive a response, converts the response from JSON string back
# to a dictionary using `from_json`, and returns this dictionary.
async def send(msg: dict, conn: ClientConnection) -> dict:
    await conn.send(to_json(msg))  # Send the JSON string representation of the message
    return from_json(await conn.recv())  # Receive the response and convert it from JSON string to dictionary
