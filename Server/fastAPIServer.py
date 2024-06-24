# External imports
from fastapi import WebSocket, WebSocketDisconnect
from json import loads, JSONDecodeError

# Own modules
from Server.connection_manager import AbstractConnectionManager
from Server.lobby import Lobby
from Server.lobby_manager import LobbyManager
from Tools.Game_Config.difficulty import EDifficulty
from Tools.Game_Config.mode import EGameMode
from Tools.dynamic_imports import Importer
from Tools.language_handler import LanguageHandler
from Tools.rcode import RCODE
from Tools.languages import LANGUAGE


class FastAPIServer(AbstractConnectionManager):
    def __init__(self, manager: LobbyManager, msg_builder: LanguageHandler, importer: Importer):
        super().__init__(msg_builder)
        self.manager: LobbyManager = manager
        self.importer: Importer = importer
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
        lobby: Lobby = self.manager.get_lobby(websocket)
        if lobby:
            lobby.force_leave(websocket)
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
        finally:
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
                    return await self.send_response(client=client, code=RCODE.L_LOBBYNOTEXIST, data={"key": lobby_key})
                lobby_key = read_object.get("key")
                pos = read_object.get("pos")
                if lobby.game_running:
                    if pos != "sp":
                        return await self.send_response(client=client, code=RCODE.L_RUNNINGNOJOIN)
                if not self.manager.join_lobby(lobby_key, client, pos):
                    return await self.send_response(client=client, code=RCODE.L_JOINFAILURE, data={"key": lobby_key})
                await self.broadcast_response(client_list=lobby.get(None), code=RCODE.L_JOINED,
                                              data={"pos": self.manager.get_pos_of_client(client)})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "leave":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                pos = self.manager.get_pos_of_client(client)
                client_list = lobby.get(None)
                if not self.manager.leave_lobby(client, False):
                    if lobby.game_running and lobby.in_lobby(client):
                        return await self.send_response(client=client, code=RCODE.L_NOLEAVEACTIVPLAYER)
                await self.broadcast_response(client_list=client_list, code=RCODE.L_LEFT,
                                              data={"pos": pos})
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            case "swap":
                pos: str = read_object.get("pos")
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby is None:
                    return await self.send_response(client=client, code=RCODE.L_CLIENTNOTINLOBBY)
                if lobby.game_running:
                    if lobby.in_lobby(client):
                        return await self.send_response(client=client, code=RCODE.L_NOSWAP)
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
            case "games":
                lobby: Lobby = self.manager.get_lobby(client)
                if lobby:  # success
                    await self.send_response(client=client, code=RCODE.L_GAMES,
                                             data={"games": [k for k in self.importer.get_games().keys()]})
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
        if lobby is None:
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
        if command_key == "create":
            lobby.game = data.get("game")
            lobby.difficulty = EDifficulty.get(data.get("difficulty"))
            lobby.mode = EGameMode.get(data.get("mode"))
            if self.importer.get_games().get(lobby.game) is None:
                return await self.send_response(client=client, code=RCODE.INVALIDGAME,
                                                data={"game": data.get("game"),
                                                      "available": [m for m in self.importer.get_games().keys()]})
            if lobby.difficulty is None:
                return await self.send_response(client=client, code=RCODE.INVALIDDIFFICULTY,
                                                data={"difficulty": data.get("difficulty"),
                                                      "available": [m.name for m in EDifficulty]})
            if lobby.mode is None:
                return await self.send_response(client=client, code=RCODE.INVALIDDIFFICULTY,
                                                data={"mode": data.get("mode"),
                                                      "available": [m.name for m in EGameMode]})

        if command_key in ["create", "new_game"]:  # prevent a game to start without enough player
            missing = []
            mode_checks = {
                0: [("P1", True, " not connected!"), ("P2", True, " not connected!")],          # player_vs_player
                1: [("P1", True, " not connected!"), ("P2", False, " needs to be empty!")],     # player_vs_KIM
                2: [("P1", False, " needs to be empty!"), ("P2", True, " not connected!")],     # KIM_vs_player
                3: [("P1", True, " not connected!"), ("P2", True, " not connected!")],          # playerai_vs_playerai
                4: [("P1", True, " not connected!"), ("P2", False, " needs to be empty!")],     # playerai_vs_KIM
                5: [("P1", False, " needs to be empty!"), ("P2", True, " not connected!")]      # KIM_vs_playerai
            }

            for player, should_be_connected, message in mode_checks.get(lobby.mode.value, []):
                if should_be_connected and getattr(lobby, player.lower()) is None:
                    missing.append([player, message])
                elif not should_be_connected and getattr(lobby, player.lower()) is not None:
                    missing.append([player, message])

            if missing:
                data = {i[0]: i[1] for i in missing}
                return await self.send_response(client=client, code=RCODE.L_LOBBYNOTREADY, data=data)

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
