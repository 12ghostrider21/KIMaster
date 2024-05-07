from fastAPIServer import FastAPIServer
import sys


def main():
    # Extract command-line arguments or use default values
    port_SocketServer = sys.argv[1] if len(sys.argv) > 1 else "12345"
    port_SocketServer = int(port_SocketServer)
    port_FastAPI = sys.argv[2] if len(sys.argv) > 2 else "8000"
    port_FastAPI = int(port_FastAPI)
    host_SocketServer = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    host_FastAPI = sys.argv[4] if len(sys.argv) > 4 else "0.0.0.0"

    # Initialize and run FastAPI server
    fastapi_server = FastAPIServer()
    fastapi_server.start(host_SocketServer=host_SocketServer,
                         host_FastAPI=host_FastAPI,
                         port_FastAPI=port_FastAPI,
                         port_SocketServer=port_SocketServer)


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 5:
        main()
    else:
        # Print usage and exit if arguments are incorrect
        print("Usage: python StartServer.py port_SocketServer:12345 port_FastAPI:8000 host_SocketServer host_FastAPI")
        sys.exit(1)
