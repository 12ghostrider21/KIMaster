import asyncio
from os import environ
from game_client import GameClient


def main():
    port = int(environ.get("SERVER_PORT", 8000))
    host = environ.get("SERVER_HOST", "localhost")
    key = environ.get("LOBBY_KEY", "")

    client = GameClient(host=host, port=port, key=key)
    asyncio.run(client.run())


if __name__ == "__main__":
    main()
