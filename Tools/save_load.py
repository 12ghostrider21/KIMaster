import pickle
from pickle import PickleError
from GameClient.arena import Arena

def save_game_to_file(arena: Arena) -> bytes | None:
    """
    Serializes an Arena object to a bytes stream.

    Args:
        arena (Arena): The Arena object to serialize.

    Returns:
        bytes | None: The serialized byte stream of the Arena object, or None if an error occurs.
    """
    try:
        return pickle.dumps(arena)
    except PickleError:
        # Log the exception or handle it as necessary
        return None

def load_game_from_file(bytestream) -> Arena | None:
    """
    Deserializes a bytes stream to an Arena object.

    Args:
        bytestream (bytes): The byte stream to deserialize.

    Returns:
        Arena | None: The deserialized Arena object, or None if an error occurs.
    """
    try:
        return pickle.loads(bytestream)
    except PickleError:
        # Log the exception or handle it as necessary
        return None
