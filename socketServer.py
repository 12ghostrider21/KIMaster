from json.decoder import JSONDecodeError
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from Datatypes import RESPONSE
from lobby import LobbyManager


class SocketServer:
    def __init__(self):
        self.__app = FastAPI()
        self.lobby_manager: LobbyManager = LobbyManager()

        @self.__app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            connection = await self.connect(websocket)
            while connection:
                try:

                    # User < - fastApiServer -> SocketServer < - > Game_client
                    #                *              <->                  *



                    readObject = await websocket.receive_text()
                    print(readObject)
                    await websocket.send_text(readObject)
                except WebSocketDisconnect as e:
                    print("websocket closes...", e)
                    break
            await self.disconnect(websocket)

    # *************************************************************************************************************

    # *************************************************************************************************************

    async def connect(self, client: WebSocket):
        await client.accept()

    async def send_cmd(self, client: WebSocket, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    async def send_response(self, client: WebSocket, response_code: RESPONSE, response_msg: str, data: dict | None = None):
        cmd = {"response_code": response_code.value, "response_msg": response_msg}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    async def disconnect(self, game_client: WebSocket):
        if game_client.client_state == WebSocketState.CONNECTED:
            await game_client.close(code=1000, reason="Server initiated closure")
        self.lobby_manager.disconnect_game_client(game_client)
        print(f"GameClient disconnected as: {game_client}")

    def run(self, host: str, port: int):
        import uvicorn
        print(f"SocketServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)
