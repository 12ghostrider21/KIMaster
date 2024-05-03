from code.backend.api.SocketServer import Server
from code.backend.api.FastAPIServer import FastAPIServer


if __name__ == "__main__":
    fastapi_server = FastAPIServer(Server())
    fastapi_server.run()
