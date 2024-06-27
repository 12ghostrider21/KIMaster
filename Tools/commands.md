# Statuscode-Interval

## General success = 0 - 49
- **LANGUAGECHANGED** = 0, "Language has been changed successfully.
- **INVALIDLANGUAGE** = 1, "Selected language not found."

## General error = 50 - 99
- **INTERNALERROR** = 50, "Critical internal error."
- **INVALIDJSON** = 51, "The received message is not a valid JSON."
- **COMMANDNOTFOUND** = 52, "The specified command does not exist."
- **INVALIDGAME** = 53, "The specified game does not exist."
- **INVALIDDIFFICULTY** = 54, "The specified difficulty level does not exist."
- **INVALIDMODE** = 55, "The specified game mode does not exist."

## Lobby success = 100 - 149
- **L_CREATED** = 100, "Lobby has been successfully created."
- **L_JOINED** = 101, "Player has successfully joined the lobby."
- **L_LEFT** = 102, "Player has successfully left the lobby."
- **L_SWAPPED** = 103, "Player has successfully swapped positions within the lobby."
- **L_POS** = 104, "Current position in the lobby has been successfully retrieved."
- **L_STATUS** = 105, "Lobby status has been successfully retrieved."
- **L_GAMES** = 106, "List of games has been successfully retrieved."

## Lobby error = 150 - 199
- **L_CLIENTALREADYINLOBBY** = 150, "Client is already in a lobby and cannot join multiple lobbies."
- **L_LOBBYNOTEXIST** = 151, "The specified lobby does not exist."
- **L_JOINFAILURE** = 152, "Failed to join the lobby."
- **L_CLIENTNOTINLOBBY** = 153, "The specified client is not in the lobby."
- **L_POSUNKNOWN** = 154, "The position within the lobby is unknown."
- **L_POSOCCUPIED** = 155, "The position within the lobby is already occupied."
- **L_LOBBYKEYINVALID** = 156, "Invalid or missing lobby key."
- **L_LOBBYNOTREADY** = 157, "Lobby does not have enough players to start."
- **L_NOLEAVEACTIVPLAYER** = 158, "Client cannot leave an active game as a player."
- **L_NOSWAP** = 159, "Client cannot swap positions in an active game as a player."
- **L_RUNNINGNOJOIN** = 160, "Lobby is already running; join only as a spectator."

## Play success = 200 - 249
- **P_ARENAINIT** = 200, "Arena has been successfully initialized."
- **P_EVAL** = 201, "Play evaluation has been successfully performed."
- **P_GAMEOVER** = 202, "Game has ended successfully."
- **P_EVALOVER** = 203, "Evaluation process has concluded successfully."
- **P_BOARD** = 205, "Game board has been successfully retrieved or updated."
- **P_REPRESENTATION** = 206, "Game representation has been successfully retrieved."
- **P_VALIDMOVE** = 207, "A valid move has been made."
- **P_MOVES** = 208, "List of possible moves has been successfully retrieved."
- **P_VALIDUNDO** = 209, "A valid undo action has been performed."
- **P_SURRENDER** = 210, "A player has surrendered successfully."
- **P_BLUNDER** = 211, "A blunder (serious mistake) has been identified in the play."
- **P_BLUNDERLIST** = 212, "List of blunders has been successfully retrieved."
- **P_TIMELINE** = 214, "Timeline of events in the game has been successfully retrieved."
- **P_NOVALIDMOVES** = 215, "Player does not have any valid moves left."
- **P_STEP** = 216, "Step forward in the timeline."
- **P_UNSTEP** = 217, "Step backward in the timeline."
- **P_PLAYER** = 218, "Sends the current active player."

## Play error = 250 - 299
- **P_NOGAMECLIENT** = 250, "No game client available; try again."
- **P_NOPERMISSION** = 251, "Player does not have permission to perform the action."
- **P_NOTRUNNING** = 252, "Game has not been initialized."
- **P_ARGS** = 253, "Invalid arguments provided."
- **P_STILLRUNNING** = 254, "Game is still running; requested action cannot be performed."
- **P_NOMOVE** = 255, "No move has been made."
- **P_INVALIDMOVE** = 256, "The move made is invalid."
- **P_INVALIDPOS** = 257, "The specified position is invalid."
- **P_NOUNDO** = 258, "No undo action available."
- **P_INVALIDUNDO** = 259, "The undo action attempted is invalid."
- **P_NOTIMELINE** = 260, "No timeline available."
- **P_INVALIDTIMELINE** = 261, "The specified timeline is invalid."
- **P_NOEVALUATION** = 262, "No evaluation available."
- **P_INVALIDEVALUATION** = 263, "The evaluation attempted is invalid."
- **P_GAMENOTAVAILABLE** = 265, "The specified game is not available."
- **P_NOGAMEINIT** = 266, "Create a game first."
- **P_EVALNUMOVER** = 267, "The selected number is too high."
- **P_NOTYOURTURN** = 268, "Player tried to make a move out of turn."

## Debug success = 300 - 349
- **D_CONTAINER** = 300, "List all active containers."
- **D_TOGGLECLIENT** = 301, "Toggle debug mode of the game client."

# Universal Messages
GameClient status change -> message to Server
```json
{"command": "game_client", "command_key": "state", "state": $LobbyState}
```
Response message language change -> message to Server
```json
{"command": "language", "command_key": "lang", "lang": $Language}
```
User sends not a json 
```json
{"response_code": 51, "response_msg": "Invalid JSON format."}
```
User sends unknown command
```json
{"response_code": 52, "response_msg": "Specified command not found.", "command": $command}
```
(Gameclient crashed or closed -> message to Client)
```json
{"response_code": 53, "response_msg": "GameClient error"}
```
# Special messages
| code  | Return            | Discription |
|-------|-------------------|-------------|
| 202   | result, turn      | Broadcast Gameover message to every active client in lobby.|
| 205   | board             | Will send current board to spezific player in lobby.|
| 206   | representation    | Broadcast the board representation to every active client in lobby terminal.|
| None  | image             | Will send the board image as bytestream to every active client in lobby.|
| None  | image             | Will send the borad iamge as bytestream to spezific client in lobby.|

# Lobby Commands
| key       | Parameter   | Success code| Error code    | Return      | Discription |
|-----------|-------------|-------------|---------------|-------------|-------------|
| create    | None        | 100         | 150           | key         | Will create a new Lobby and send new lobby_key back.|
| join      | key, [pos]  | 101         | 150, 151, 160 | None        | Join lobby with **key** on - **Pos** |
| leave     | None        | 102         | 153, 158      | None        | Leave a lobby. |
| swap      | pos         | 103         | 153, 154, 155, 159 | None        | Change position in lobby to - **Pos** if not occupied or playing. [p1, p2, sp]|
| pos       | None        | 104         | 153           | pos         | Returns the current position in a lobby of client.|
| status    | None        | 105         | 153           | P1, P2, Spectators, GameClient, GameState, key | Returns the current state of the lobby the client is currently in.|
**Parameter** with "[]" do not need to be spezified.

# Play Commands
| key       | Parameter   | Success code| Error code        | Return      | Discription |
|-----------|-------------|-------------|-------------------|-------------|-------------|
|valid_moves| pos         | 208         | 252, 257          | image       | Returns a new image from game with hightlighted positions of possible moves.
| make_move | pos         | 207         | 252, 255, 256     | None        | Make a move on current game. - **Pos** can be an int or an tuple[int, int]. Like [from, to] [2, 3]|
| undo_move | num         | 209         | 252, 258, 259     | None        | Undo the last **num** moves.|
| surrender | None        | 210         | 252               | result      | Client surrender active game and a broadcast message get triggered.|
| quit      | None        | 211         | 254               | None        | The GameClient will disconnect and the lobby can not be played anymore. All play data gets lost.|
| new_game  | None        | 200         | 52, 252, 254      | None        | Will start a new Game with last set configuration.|
| blunder   | None        | 212, 213    | 252               | blunder     | After finished game, **blunder** will show the bad moves the client did.|
| timeline  | num         | 214         | 252, 260, 261     | represantation, image | After finished game.**timeline** display the **num** move of the game.|
| step      | None        | 214         | 252, 261          | represantation, image | After finished game. Step to next **timeline** index.|
| unstep    | None        | 214         | 252, 261          | represantation, image | After finished game. Step to bevore **timeline** index.|
| games     | None        | 215         | 52, 253           | game_name   | Will list all available games for the current lobby.|
| create    | game, mode, difficulty|200| 52, 254, 265, 157 | None        | Will initialise a **game_config** and start the game.|
| evaluate  | game, difficulty, num | 201, 203 | 254, 262, 263, 157 | wins, losses, draws |Will play up to **num** [max=100] games in a row and returns the evaluatuin stats.|
| stop_evaluate | None    | 203         | 252           | wins, losses, draws | Will stop a active Evaluation and returns evaluation stats

### Parameter difficulty:
| difficulty | MCTS dept |
| ---------- | --------- |
| easy       | 75        |
| medium     | 175       |
| hard       | 275       |
### Parameter mode:
  - player_vs_player
  - player_vs_ai
  - playerai_vs_ai
  - playerai_vs_playerai
### Paramter games:
  - Connect4
  - Othello
  - TicTacToe
  - Checkers
  - Go
  - Nim

# Debug Commands
| key       | Parameter   | Success code| Error code    | Return      | Discription |
|-----------|-------------|-------------|---------------|-------------|-------------|
| active_container | None | 300         | None          | count       | Will return every active container and the total container count. [Docker container ls] |
|game_client| None        | 301         | None          | debug       | Will aktivate debug mode of every new GameClient. GameClient will not be deleted.|

# Examples
## Lobby:
```json
{"command": "lobby", "command_key": "create"}
```
```json
{"command": "lobby", "command_key": "join", "key": "lobby_key"}
```
```json
{"command": "lobby", "command_key": "leave"}
```
```json
{"command": "lobby", "command_key": "swap", "pos": "sp"}
```
```json
{"command": "lobby", "command_key": "pos"}
```
```json
{"command": "lobby", "command_key": "status"}
```
## Lobby:
```json
{"command": "play", "command_key": "create", "game": "Connect4", "mode": "player_vs_ai", "difficulty": "hard"}
```
```json
{"command": "play", "command_key": "valid_moves", "pos": 2}
```
```json
{"command": "play", "command_key": "make_move", "move": 4}
```
```json
{"command": "play", "command_key": "undo_move", "num": 1}
```
```json
{"command": "play", "command_key": "surrender"}
```
```json
{"command": "play", "command_key": "quit"}
```
```json
{"command": "play", "command_key": "new_game"}
```
```json
{"command": "play", "command_key": "blunder"}
```
```json
{"command": "play", "command_key": "timeline", "num": 0}
```
```json
{"command": "play", "command_key": "step"}
```
```json
{"command": "play", "command_key": "unstep"}
```
```json
{"command": "play", "command_key": "games"}
```
```json
{"command": "play", "command_key": "evaluate", "game": "Connect4", "difficutly": "hard", "num": 50}
```
```json
{"command": "play", "command_key": "stop_evaluate"}
```
## Debug
```json
{"command": "debug", "command_key": "active_container"}
```
```json
{"command": "debug", "command_key": "game_client"}
```