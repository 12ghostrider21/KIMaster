# External imports
from fastapi import WebSocket, WebSocketDisconnect
from json import loads, JSONDecodeError

# Own modules
from Server.connection_manager import AbstractConnectionManager
from Server.lobby import Lobby
from Server.lobby_manager import LobbyManager
from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode
from Tools.language_handler import LanguageHandler
from Tools.rcode import RCODE
from Tools.languages import LANGUAGE


class FastAPIServer(AbstractConnectionManager):
    def __init__(self, manager: LobbyManager, msg_builder: LanguageHandler):
        super().__init__(msg_builder)
        self.manager: LobbyManager = manager
        self.__command_mask: list[str] = ["command", "command_key", "pos", "key", "mode", "game", "difficulty", "num",
                                          "move", "lang"]
        self.__play_mask: list[str] = ["create", "valid_moves", "make_move", "undo_move", "surrender", "quit",
                                       "new_game", "blunder", "timeline", "step", "unstep", "evaluate", "stop_evaluate",
                                       "games"]

    # Method to connect a WebSocket client
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    # Method to disconnect a WebSocket client
    async def disconnect(self, websocket: WebSocket):
        self.manager.leave_lobby(websocket)
        self.active_connections.remove(websocket)

    # Main endpoint for WebSocket connections
    async def websocket_endpoint(self, client: WebSocket):
        await self.connect(client)
        try:
            while True:
                try:
                    read_object = await client.receive_json()
                    if isinstance(read_object, str):
                        read_object = loads(read_object)
                    # Filter read_object based on allowed keys
                    read_object = {k: v for k, v in read_object.items() if k in self.__command_mask}
                except JSONDecodeError:
                    await self.send_response(client, RCODE.INVALIDJSON)
                    continue

                command = read_object.get("command")
                match command:
                    case "debug":
                        await self.handle_debug_command(client, read_object)
                    case "lobby":
                        await self.handle_lobby(client, read_object)
                    case "play":
                        await self.handle_play_command(client, read_object)
                    case "client":
                        await self.handle_client(client, read_object)
                    case _:
                        await self.send_response(client, RCODE.COMMANDNOTFOUND, {"command": command})
        except WebSocketDisconnect:
            await self.disconnect(client)

    # *****************************************************************************************************************
    # handle debug
    # *****************************************************************************************************************
    async def handle_debug_command(self, client: WebSocket, read_object: dict):
        command_key = read_object.get("command_key")
        match command_key:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "active_container":
                await self.send_response(client=client, code=RCODE.D_CONTAINER,
                                         data=self.manager.docker.list_containers())
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "game_client":
                self.manager.docker.debug = not self.manager.docker.debug
                await self.send_response(client=client, code=RCODE.D_TOGGLECLIENT,
                                         data={"debug": self.manager.docker.debug})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case _:
                await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND, data={"command": command_key})

    # *****************************************************************************************************************
    # handle lobby
    # *****************************************************************************************************************
    async def handle_lobby(self, client: WebSocket, read_object: dict):
        command_key = read_object.get("command_key")
        match command_key:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "create":
                lobby = self.manager.get_lobby(client)
                if lobby:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTALREADYINLOBBY)
                new_lobby_key = self.manager.create_lobby()
                self.manager.join_lobby(new_lobby_key, client, "p1")
                await self.send_response(client=client, code=RCODE.L_CREATED, data={"key": new_lobby_key})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "join":
                lobby_key = read_object.get("key")
                lobby: Lobby = self.manager.get_lobby(lobby_key)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTALREADYINLOBBY)
                lobby_key = read_object.get("key")
                pos = read_object.get("pos")
                if not self.manager.lobby_exist(lobby_key):
                    return await self.send_response(client=client, code=RCODE.L_LOBBYNOTEXIST, data={"key": lobby_key})
                if not self.manager.join_lobby(lobby_key, client, pos):
                    return await self.send_response(client=client, code=RCODE.L_JOINFAILURE, data={"key": lobby_key})
                await self.send_response(client=client, code=RCODE.L_JOINED,
                                         data={"key": lobby_key, "pos": self.manager.get_pos_of_client(client)})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "leave":
                if not self.manager.leave_lobby(client):
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                await self.send_response(client=client, code=RCODE.L_LEFT)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "swap":
                pos: str = read_object.get("pos")
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                if pos not in ["p1", "p2", "sp"]:
                    return await self.send_response(client=client, code=RCODE.L_POSUNKNOWN, data={"pos": pos})
                if not self.manager.swap_to(pos, client):
                    return await self.send_response(client=client, code=RCODE.L_POSOCCUPIED, data={"pos": pos})
                await self.send_response(client=client, code=RCODE.L_SWAPPED, data={"pos": pos})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "pos":
                pos: str = self.manager.get_pos_of_client(client)
                if pos:
                    await self.send_response(client=client, code=RCODE.L_POS, data={"pos": pos})
                else:  # client not in lobby
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "status":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby:  # success
                    await self.send_response(client=client, code=RCODE.L_STATUS, data=lobby.status())
                else:  # client not in lobby
                    await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case _:
                await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND, data={"command_key": command_key})

    # *****************************************************************************************************************
    # handle play
    # *****************************************************************************************************************
    async def handle_play_command(self, client: WebSocket, read_object: dict):
        lobby = self.manager.get_lobby(client)
        if not lobby:
            return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
        if not lobby.game_client:
            return await self.send_response(client=client, code=RCODE.P_NOGAMECLIENT)
        pos: str = self.manager.get_pos_of_client(client)
        if pos == "sp":
            return await self.send_response(client=client, code=RCODE.P_NOPERMISSION)
        data = {"p_pos": pos, "key": lobby.key, **read_object}
        command_key = read_object.get("command_key")
        if command_key not in self.__play_mask:
            return await self.send_response(client=client, code=RCODE.COMMANDNOTFOUND,
                                            data={"command_key": command_key})
        if command_key == "Create":
            lobby.game = data.get("game")
            lobby.difficulty = EDifficulty.get(data.get("difficulty"))
            lobby.mode = EGameMode.get(data.get("mode"))
        await self.send_cmd(lobby.game_client, "play", command_key, data)

    # *****************************************************************************************************************
    # handle client
    # *****************************************************************************************************************
    async def handle_client(self, client: WebSocket, read_object: dict):
        command_key = read_object.get("command_key")
        match command_key:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "language":
                lang: str = read_object.get("lang")
                for e in LANGUAGE:
                    if e.name.lower() == lang.lower():
                        self.language = e
                        await self.send_response(client, RCODE.LANGUAGECHANGED, {"lang": self.language.name})
                        return
                await self.send_response(client, RCODE.INVALIDLANGUAGE, {"lang": lang})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case _:
                await self.send_response(client, RCODE.COMMANDNOTFOUND, {"command": command_key})
