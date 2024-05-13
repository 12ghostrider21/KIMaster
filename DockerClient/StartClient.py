import asyncio
import sys
from game_client import GameClient


def main():
    # Extract command-line arguments or use default values
    port = sys.argv[1] if len(sys.argv) > 1 else "12345"
    port = int(port)
    host = sys.argv[2] if len(sys.argv) > 2 else "localhost"
    key = sys.argv[3] if len(sys.argv) > 3 else "29636243f2c92c7ceef0e9a38686c028617e03d53317546721c52f39a3365d53"


    game_client = GameClient(port=port, host=host, key=key).run()
    asyncio.get_event_loop().run_until_complete(game_client)


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 4:
        main()
    else:
        # Print usage and exit if arguments are incorrect
        print("Usage: python StartClient.py port host key")
        sys.exit(1)
