from os import environ
from fastapi import FastAPI
import uvicorn
from fastAPIServer import FastAPIServer
from socketServer import SocketServer
from Tools.language_handler import LanguageHandler


def main():
    """
    Main function to set up and run the FastAPI application.

    Initializes the language handler, socket server, and FastAPI server.
    Configures WebSocket endpoints and runs the application using Uvicorn.
    """
    # Create a FastAPI application instance
    app = FastAPI()

    # Initialize LanguageHandler with a path to the language file
    msg_builder = LanguageHandler("../Tools/language.csv")

    # Initialize the SocketServer with the language handler
    socket_server = SocketServer(msg_builder)

    # Initialize the FastAPIServer with the socket manager and language handler
    fast_api_server = FastAPIServer(socket_server.manager, msg_builder)

    # Define WebSocket endpoints
    app.websocket("/ws")(fast_api_server.websocket_endpoint)  # WebSocket endpoint for FastAPIServer
    app.websocket("/game")(socket_server.websocket_endpoint)  # WebSocket endpoint for SocketServer

    # Run the FastAPI application using Uvicorn with the specified host and port from environment variables
    uvicorn.run(app, host=environ["SERVER_HOST"], port=int(environ["SERVER_PORT"]))


if __name__ == "__main__":
    # If this script is run directly, execute the main function
    main()
