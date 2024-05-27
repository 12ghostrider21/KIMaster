import asyncio
import os
from game_client import GameClient


def main():
    # Extract command-line arguments or use default values
    try:
        port = int(os.environ["SOCKET_SERVER_PORT"])
        host = os.environ["HOST_OF_API"]
        key = os.environ["LOBBY_KEY"]
    except Exception:
        port = 12345
        host = "0.0.0.0"
        key = "43204118ec74bc8cd7102542738d2e529cdc19bf2ffa5614fde000e95188b3f0"

    game_client = GameClient(port=port, host=host, key=key).run()
    asyncio.get_event_loop().run_until_complete(game_client)


if __name__ == "__main__":
    main()

