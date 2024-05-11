import json
from json.decoder import JSONDecodeError
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from datatypes import RESPONSE
from lobby import LobbyManager, Lobby


class SocketServer:
    def __init__(self):
        self.__app = FastAPI()
        self.lobby_manager: LobbyManager = LobbyManager()

        @self.__app.websocket("/ws")
        async def websocket_endpoint(game_client: WebSocket):
            await self.connect(game_client)
            lobby: Lobby = self.lobby_manager.lobby_of_game_client(game_client)
            while True:
                try:
                    readObject: dict = await game_client.receive_json()
                except json.decoder.JSONDecodeError:
                    await self.send_response(game_client, RESPONSE.ERROR, "Received data is not a correct json!")
                    continue
                except WebSocketDisconnect:
                    break

                response = readObject.get("response_code")
                if response:
                    p = None
                    match readObject.get("player_pos"):
                        case "p1":
                            p = lobby.p1
                        case "p2":
                            p = lobby.p2
                        case _:
                            raise TypeError(readObject.get("player_pos"))
                    await self.send_response(p,
                                             response_code=response,
                                             response_msg=readObject.get("response_msg"),
                                             data=readObject.get("data"))
                    continue

                # command handling
                command: str = readObject.get("command")
                match command:
                    case "exit":
                        break
                    case "login":
                        lobby_key: str = readObject.get("key")
                        lobby: Lobby = self.lobby_manager.lobbies.get(lobby_key)
                        if lobby is None:
                            await self.send_response(game_client, RESPONSE.ERROR, "Lobby does not exist", {"key": lobby_key})
                            continue
                        lobby.game_client = game_client
                        await self.send_response(game_client, RESPONSE.SUCCESS, "Joined lobby!", {"key": lobby_key})
                    case _:
                        await self.send_response(game_client, RESPONSE.ERROR, f"Command: '{command}' not found!")
            await self.disconnect(game_client)

    # *************************************************************************************************************

    # *************************************************************************************************************

    async def connect(self, client: WebSocket):
        await client.accept()

    async def send_cmd(self, client: WebSocket, command: str, command_key: str, data: dict | None = None):
        cmd = {"command": command, "command_key": command_key}
        if data is not None:
            cmd.update(data)
        await client.send_json(cmd)

    async def send_response(self, client: WebSocket, response_code: RESPONSE, response_msg: str,
                            data: dict | None = None):
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
