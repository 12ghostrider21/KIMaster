import asyncio
import os
from game_client import GameClient


def main():
    # Extract command-line arguments or use default values
    port = int(os.environ["PORT_TO_GAME_CLIENT"])
    host = os.environ["HOST_SOCKET_SERVER"]
    key = os.environ["LOBBY_KEY"]

    game_client = GameClient(port=port, host=host, key=key).run()
    asyncio.get_event_loop().run_until_complete(game_client)


if __name__ == "__main__":
    main()

