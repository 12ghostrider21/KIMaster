from asyncio import get_event_loop
from os import environ
from game_client import GameClient


def main():
    port = int(environ["SERVER_PORT"])
    host = environ["SERVER_HOST"]
    key = environ["LOBBY_KEY"]

    client = GameClient(host=host, port=port, key=key)
    get_event_loop().run_until_complete(client.run())


if __name__ == "__main__":
    main()
