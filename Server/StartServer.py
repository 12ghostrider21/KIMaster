from fastAPIServer import FastAPIServer
import os


def main():
    """
    Main function to initialize and run the Server.

    This function retrieves the necessary environment variables to configure
    the FastAPI server and socket server. It initializes the FastAPIServer
    object and starts the server with the specified configuration.

    Environment Variables:
    - SOCKET_SERVER_PORT: The port number for the socket server.
    - HOST_OF_API: The host address for both the FastAPI and socket server.
    - FAST_API_PORT: The port number for the FastAPI server.

    Raises:
    - KeyError: If any of the required environment variables are not set.
    - ValueError: If the environment variables for port numbers are not valid integers.
    """
    # Retrieve and convert environment variables
    port_socket_server = int(os.environ["SOCKET_SERVER_PORT"])
    host_socket_server = os.environ["HOST_OF_API"]
    port_fast_api = int(os.environ["FAST_API_PORT"])
    host_fast_api = os.environ["HOST_OF_API"]

    # Initialize and run FastAPI server
    fastapi_server = FastAPIServer()
    fastapi_server.start(
        host_socket_server=host_socket_server,
        host_fast_api=host_fast_api,
        port_fast_api=port_fast_api,
        port_socket_server=port_socket_server
    )


if __name__ == "__main__":
    main()
