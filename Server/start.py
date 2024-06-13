from os import environ

from fastapi import FastAPI
import uvicorn
from fastAPIServer import FastAPIServer
from socketServer import SocketServer
from Tools.language_handler import LanguageHandler


def main():
    app = FastAPI()
    msg_builder = LanguageHandler("../Tools/language.csv")
    socket_server = SocketServer(msg_builder)
    fast_api_server = FastAPIServer(socket_server.manager, msg_builder)
    app.websocket("/ws")(fast_api_server.websocket_endpoint)
    app.websocket("/game")(socket_server.websocket_endpoint)

    uvicorn.run(app, host=environ["SERVER_HOST"], port=int(environ["SERVER_PORT"]))


if __name__ == "__main__":
    main()
