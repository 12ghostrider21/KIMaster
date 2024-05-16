from fastAPIServer import FastAPIServer
import sys


def main():
    # Extract command-line arguments or use default values
    port_socket_server = sys.argv[1] if len(sys.argv) > 1 else "12345"
    port_socket_server = int(port_socket_server)
    port_fast_api = sys.argv[2] if len(sys.argv) > 2 else "8000"
    port_fast_api = int(port_fast_api)
    host_socket_server = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    host_fast_api = sys.argv[4] if len(sys.argv) > 4 else "0.0.0.0"

    # Initialize and run FastAPI server
    fastapi_server = FastAPIServer()
    fastapi_server.start(host_socket_server=host_socket_server,
                         host_fast_api=host_fast_api,
                         port_fast_api=port_fast_api,
                         port_socket_server=port_socket_server)


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 5:
        main()
    else:
        # Print usage and exit if arguments are incorrect
        print("Usage: python StartServer.py port_SocketServer:12345 port_FastAPI:8000 host_SocketServer host_FastAPI")
        sys.exit(1)
