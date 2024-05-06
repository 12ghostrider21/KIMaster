import asyncio
import sys
from Arena import Arena


def main():
    # Extract command-line arguments or use default values
    port = sys.argv[1] if len(sys.argv) > 1 else "12345"
    port = int(port)
    host = sys.argv[2] if len(sys.argv) > 2 else "localhost"
    key = sys.argv[3] if len(sys.argv) > 3 else "no key"

    asyncio.get_event_loop().run_until_complete(Arena(port=port, host=host).readLoop())


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 5:
        main()
    else:
        # Print usage and exit if arguments are incorrect
        print("Usage: python StartClient.py port host")
        sys.exit(1)
