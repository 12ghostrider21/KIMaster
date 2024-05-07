from json.decoder import JSONDecodeError
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from lobby import LobbyManager


class SocketServer:
    def __init__(self):
        self.__app = FastAPI()
        self.lobby_manager: LobbyManager = LobbyManager()

        @self.__app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.connect(websocket)
            while True:
                try:
                    readObject = await websocket.receive_text()
                    print(readObject)
                    await websocket.send_text(readObject)
                except WebSocketDisconnect as e:
                    print("websocket closes...", e)
                    break
            await self.disconnect(websocket)

    # *************************************************************************************************************

    # *************************************************************************************************************

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print(f"GameClient connected with: {websocket}")

    async def send_image(self, image_bytes: bytes, websocket: WebSocket):
        await websocket.send_bytes(image_bytes)

    async def send_cmd(self, websocket: WebSocket, command: str, command_key: str, data: dict | None = None):
        if data is None:
            data = {}
        cmd = {"command": command, "command_key": command_key}
        cmd.update(data)  # add data if used
        await websocket.send_json(cmd)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def disconnect(self, game_client: WebSocket):
        if game_client.client_state == WebSocketState.CONNECTED:
            await game_client.close(code=1000, reason="Server initiated closure")
        print(f"GameClient disconnected as: {game_client}")

    def run(self, host: str, port: int):
        import uvicorn
        print(f"SocketServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)
