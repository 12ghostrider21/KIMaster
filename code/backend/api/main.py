from SocketServer import Server
from FastAPIServer import FastAPIServer

if __name__ == "__main__":
    fastapi_server = FastAPIServer(Server())
    fastapi_server.run()
