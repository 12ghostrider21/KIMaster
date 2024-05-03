from code.backend.api.server.SocketServer import Server
from code.backend.api.server.FastAPIServer import FastAPIServer
import sys

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python main.py port_SocketServer port_FastAPI host_SocketServer, host_FastAPI")
        sys.exit(1)

    # Extract command-line arguments
    port_SocketServer = sys.argv[1]
    port_FastAPI = sys.argv[2]
    host_SocketServer = sys.argv[3]
    host_FastAPI = sys.argv[3]

    fastapi_server = FastAPIServer(Server(host=host_SocketServer, port=int(port_SocketServer)))
    fastapi_server.run(host=host_FastAPI, port=int(port_FastAPI))
