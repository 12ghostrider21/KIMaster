import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from threading import Thread
from starlette.websockets import WebSocketState

from Tools.e_response import EResponse
from socketServer import SocketServer


class FastAPIServer:
    def __init__(self):
        """
        Initialize the FastAPI server, set up the WebSocket endpoint, and initialize necessary attributes.
        """
        self.__app = FastAPI()
        self.socket_server = SocketServer()
        self.connected_users = []
        self.__mask = ["command", "command_key", "pos", "key", "mode", "game", "difficulty", "num", "move"]

        @self.__app.websocket("/ws")
        async def websocket_endpoint(client: WebSocket):
            """
            WebSocket endpoint to handle client connections and commands.

            Args:
                client (WebSocket): The WebSocket client connection.
            """
            await self.connect(client)
            try:
                while True:
                    try:
                        read_object = await client.receive_json()
                        if isinstance(read_object, str):
                            read_object = json.loads(read_object)

                        if any(e not in self.__mask for e in read_object):
                            await self.send_response(client, EResponse.ERROR, "Payload has an illegal key!")
                            continue

                    except json.JSONDecodeError:
                        await self.send_response(client, EResponse.ERROR, "Received payload is not a correct JSON!")
                        continue

                    command = read_object.get("command")
                    if command == "exit":
                        break
                    elif command == "play":
                        await self.handle_play_command(client, read_object)
                    elif command == "lobby":
                        await self.handle_lobby_command(client, read_object)
                    else:
                        await self.send_response(client, EResponse.ERROR, "Command not found!", {"command": command})
            except WebSocketDisconnect:
                await self.disconnect(client)

    async def connect(self, websocket: WebSocket):
        """
        Accept the WebSocket connection and add the client to the connected users list.

        Args:
            websocket (WebSocket): The WebSocket client connection.
        """
        await websocket.accept()
        self.connected_users.append(websocket)

    async def disconnect(self, client: WebSocket):
        """
        Handle disconnection of a WebSocket client.

        Args:
            client (WebSocket): The WebSocket client connection.
        """
        if client.client_state == WebSocketState.CONNECTED:
            await client.close(code=1000, reason="Server initiated closure")
        self.socket_server.lobby_manager.leave_lobby(client)
        self.connected_users.remove(client)
        print(f"FrontEnd Client disconnected: {client}")

    async def send_response(self, client: WebSocket, response_code: EResponse, response_msg: str, data=None):
        """
        Send a response to the WebSocket client.

        Args:
            client (WebSocket): The WebSocket client connection.
            response_code (EResponse): The response code.
            response_msg (str): The response message.
            data (dict, optional): Additional data to send.
        """
        cmd = {"response_code": response_code.value, "response_msg": response_msg}
        if data:
            cmd.update(data)
        await client.send_json(cmd)

    def run(self, host: str, port: int):
        """
        Run the FastAPI server.

        Args:
            host (str): The host address.
            port (int): The port number.
        """
        print(f"FastApiServer is running on {host}:{port}")
        uvicorn.run(self.__app, host=host, port=port, log_level="info", ws_ping_timeout=None)

    def start(self, host_fast_api, port_fast_api, host_socket_server, port_socket_server):
        """
        Start the FastAPI server and the Socket server on separate threads.

        Args:
            host_fast_api (str): The host address for the FastAPI server.
            port_fast_api (int): The port number for the FastAPI server.
            host_socket_server (str): The host address for the Socket server.
            port_socket_server (int): The port number for the Socket server.
        """
        Thread(target=self.socket_server.run, args=(host_socket_server, port_socket_server)).start()
        Thread(target=self.run, args=(host_fast_api, port_fast_api)).start()

    async def handle_lobby_command(self, client: WebSocket, read_object: dict):
        """
        Handle lobby-related commands.

        Args:
            client (WebSocket): The WebSocket client connection.
            read_object (dict): The command and its associated data.
        """
        command_key = read_object.get("command_key")
        lobby_manager = self.socket_server.lobby_manager

        match command_key:
            case "create":
                lobby = lobby_manager.get_lobby(client)
                if lobby:
                    await self.send_response(client, EResponse.ERROR, "Client already in a lobby!", {"key": lobby.key})
                else:
                    new_lobby_key = lobby_manager.create_lobby()
                    lobby_manager.join_lobby(new_lobby_key, client, "p1")
                    await self.send_response(client, EResponse.SUCCESS, "Lobby created!", {"key": new_lobby_key})

            case "join":
                if lobby_manager.get_lobby(client):
                    await self.send_response(client, EResponse.ERROR, "Cannot join multiple lobbies!")
                    return
                lobby_key = read_object.get("key")
                pos = read_object.get("pos")
                if not lobby_manager.lobby_exist(lobby_key):
                    await self.send_response(client, EResponse.ERROR, "Lobby does not exist!", {"key": lobby_key})
                elif lobby_manager.join_lobby(lobby_key, client, pos):
                    await self.send_response(client, EResponse.SUCCESS, "Joined lobby!", {
                        "key": lobby_key,
                        "pos": lobby_manager.get_pos_of_client(client)
                    })
                else:
                    await self.send_response(client, EResponse.ERROR, "Failed to join lobby! Maybe blocked?",
                                             {"key": lobby_key})

            case "leave":
                if not lobby_manager.leave_lobby(client):
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                else:
                    await self.send_response(client, EResponse.SUCCESS, "Client left lobby!")

            case "swap":
                pos = read_object.get("pos")
                lobby = lobby_manager.get_lobby(client)
                if not lobby:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                elif pos not in ["p1", "p2", "sp"]:
                    await self.send_response(client, EResponse.ERROR, "Position unknown!", {"pos": pos})
                elif not lobby_manager.swap_to(pos, client):
                    await self.send_response(client, EResponse.ERROR, "Position already occupied!", {"pos": pos})
                else:
                    await self.send_response(client, EResponse.SUCCESS, "Client swapped!", {"pos": pos})

            case "pos":
                pos = lobby_manager.get_pos_of_client(client)
                if not pos:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                else:
                    await self.send_response(client, EResponse.SUCCESS, "Client position is:", {"pos": pos})

            case "status":
                lobby = lobby_manager.get_lobby(client)
                if not lobby:
                    await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
                else:
                    await self.send_response(client, EResponse.SUCCESS, "Status of lobby.", lobby.status())

            case _:
                await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")

    async def handle_play_command(self, client: WebSocket, read_object: dict):
        """
        Handle play-related commands.

        Args:
            client (WebSocket): The WebSocket client connection.
            read_object (dict): The command and its associated data.
        """
        command_key = read_object.get("command_key")
        lobby = self.socket_server.lobby_manager.get_lobby(client)

        if not lobby:
            await self.send_response(client, EResponse.ERROR, "Client not in a lobby!")
            return

        game_client = lobby.game_client
        if not game_client:
            await self.send_response(client, EResponse.ERROR, "No Game client connected! Try later again.")
            return

        pos = self.socket_server.lobby_manager.get_pos_of_client(client)
        if pos == "sp":
            await self.send_response(client, EResponse.ERROR, "A spectator cannot play!")
            return

        data = {"player_pos": pos, "key": lobby.key, **read_object}

        if command_key in {"create", "valid_moves", "make_move", "undo_move", "surrender", "quit", "new_game",
                           "blunder", "timeline", "step", "unstep", "evaluate", "stop_evaluate"}:
            await self.socket_server.send_cmd(game_client, "play", command_key, data)
        else:
            await self.send_response(client, EResponse.ERROR, f"Command '{command_key}' not found!")
