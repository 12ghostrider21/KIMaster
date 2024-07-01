import asyncio  # Importing the asyncio library for asynchronous programming
from os import environ  # Importing environ from the os module to access environment variables
from game_client import GameClient  # Importing the GameClient class from the game_client module


# Define the main function which sets up and runs the GameClient
def main():
    # Retrieve the server port from the environment variables, defaulting to 8010 if not found
    port = int(environ.get("SERVER_PORT", 8010))
    # Retrieve the server host from the environment variables, defaulting to 'localhost' if not found
    host = environ.get("SERVER_HOST", "localhost")
    # Retrieve the lobby key from the environment variables, defaulting to an empty string if not found
    key = environ.get("LOBBY_KEY", "")

    # Create an instance of GameClient with the retrieved host, port, and key
    client = GameClient(host=host, port=port, key=key)
    # Use asyncio to run the client's run method, which starts the game client
    asyncio.run(client.run())


# This block ensures that the main function is called only when this script is executed directly,
# and not when it is imported as a module in another script.
if __name__ == "__main__":
    main()
