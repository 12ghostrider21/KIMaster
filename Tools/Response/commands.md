# Statuscode-Interval

# General error = 50 - 100
- **COMMANDNOTFOUND** = 50, "System is unable to find the command."
- **NONVALIDJSON** = 51, "This error indicates that the JSON data provided is not valid."
- **INTERNALERROR** = 52, "This represents an internal system error. It is a generic error that suggests something went wrong within the system."
- **GAMECLIENTQUIT** = 53, "This error occurs when the game client unexpectedly quits or disconnects."

# Lobby success = 100 -150
- **L_CREATED** = 100, "The lobby has been successfully created."
- **L_JOINED** = 101, "The player has successfully joined the lobby."
- **L_LEFT** = 102, "The player has successfully left the lobby."
- **L_SWAPPED** = 103, "The player has successfully swapped positions within the lobby."
- **L_POS** = 104, "The current position in the lobby has been successfully retrieved."
- **L_STATUS** = 105, "The status of the lobby has been successfully retrieved."

# Lobby error 150 - 200
- **L_CLIENTINLOBBY** = 150, "Client already in a lobby. Client can not join multiple lobby at the same time."
- **L_LOBBYNOTEXIST** = 151, "The specified lobby does not exist."
- **L_JOINFAILURE** = 152, "The attempt to join the lobby has failed."
- **L_CLIENTNOTEXIST** = 153, "The specified client does not exist."
- **L_POSUNKNOWN** = 154, "The position within the lobby is unknown."
- **L_POSOCCUPIED** = 155, "The position within the lobby is already occupied."
- **L_LOBBYKEY** = 156, "There is an error with the lobby key, such as an invalid or missing key."

# Play success = 200 - 250
- **P_INIT** = 200, "The play has been successfully initialized."
- **P_EVAL** = 201, "The play evaluation has been successfully performed."
- **P_GAMEOVER** = 202, "The game has ended successfully."
- **P_EVALOVER** = 203, "The evaluation process has concluded successfully."
<!--# P_TURN = 204, "Turn"  # currently not needed -->
- **P_BOARD** = 205, "The game board has been successfully retrieved or updated."
- **P_REPRESENTATION** = 206, "The game representation has been successfully retrieved."
- **P_VALIDMOVE** = 207, "A valid move has been made."
- **P_MOVES** = 208, "The list of possible moves has been successfully retrieved."
- **P_VALIDUNDO** = 209, "A valid undo action has been performed."
- **P_SURRENDER** = 210, "A player has surrendered successfully."
- **P_QUIT** = 211, "The player has quit the game successfully."
- **P_BLUNDER** = 212, "A blunder [serious mistake] has been identified in the play."
- **P_BLUNDERLIST** = 213, "The list of blunders has been successfully retrieved."
- **P_TIMELINE** = 214, "The timeline of events in the game has been successfully retrieved."
- **P_GAMES** = 215, "The list of games has been successfully retrieved."

# Play error = 250 - 300
- **P_NOGAMECLIENT** = 250, "There is no game client available. Try again."
- **P_NOPERMISSION** = 251, "The player does not have permission to perform the action."
- **P_NOINIT** = 252, "The game has not been initialized."
- **P_ARGS** = 253, "The arguments provided are invalid."
- **P_STILLRUNNING** = 254, "The game is still running and the requested action cannot be performed."
- **P_NOMOVE** = 255, "No move has been made."
- **P_INVALIDMOVE** = 256, "The move made is invalid."
- **P_INVALIDPOS** = 257, "The position specified is invalid."
- **P_NOUNDO** = 258, "No undo action is available."
- **P_INVALIDUNDO** = 259, "The undo action attempted is invalid."
- **P_NOTIMELINE** = 260, "No timeline is available."
- **P_INVALIDTIMELINE** = 261, "The timeline specified is invalid."
- **P_NOEVALUATION** = 262, "No evaluation is available."
- **P_INVALIDEVALUATION** = 263, "The evaluation attempted is invalid."
- **P_NOAVAILABLEGAMES** = 264, "No games are available."
- **P_GAMENOTAWAILABLE** = 265, "The specified game is not available."

# Debug success = 300 - 350
D_CONTAINER = 300, "The debug container has been successfully created or accessed."
D_TOGGLE = 301, "The debug toggle action has been successfully performed."

# Universal Messages
GameClient quit -> message to Server
```json
{"command": "game_client", "command_key": "quit"}
```
GameClient status change -> message to Server
```json
{"command": "game_client", "command_key": "state", "state": $LobbyState}
```
User sends unknown command
```json
{"response_code": 50, "response_msg": "Command not found", "command": $command}
```
User sends not a json 
```json
{"response_code": 51, "response_msg": "Payload is not a json"}
```
Gameclient crashed or closed -> message to Client
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
| join      | key, [pos]  | 101         | 150, 151      | None        | Join lobby with **key** on - **Pos** |
| leave     | None        | 102         | 153, 254      | None        | Leave a lobby. |
| swap      | pos         | 103         | 153, 154, 155 | None        | Change position in lobby to - **Pos** if not occupied or playing. [p1, p2, sp]|
| pos       | None        | 104         | 153           | pos         | Returns the current position in a lobby of client.|
| status    | None        | 105         | 153           | P1, P2, Spectators, GameClient, GameState, key | Returns the current state of the lobby the client is currently in.|
**Parameter** with "[]" do not need to be spezified.

# Play Commands
| key       | Parameter   | Success code| Error code    | Return      | Discription |
|-----------|-------------|-------------|---------------|-------------|-------------|
|valid_moves| pos         | 208         | 252, 257      | image       | Returns a new image from game with hightlighted positions of possible moves.
| make_move | pos         | 207         | 252, 255, 256 | None        | Make a move on current game. - **Pos** can be an int or an tuple[int, int]. Like [from, to] [2, 3]|
| undo_move | num         | 209         | 252, 258, 259 | None        | Undo the last **num** moves.|
| surrender | None        | 210         | 252           | result      | Client surrender active game and a broadcast message get triggered.|
| quit      | None        | 211         | 254           | None        | The GameClient will disconnect and the lobby can not be played anymore. All play data gets lost.|
| new_game  | None        | 200         | 52, 252, 254  | None        | Will start a new Game with last set configuration.|
| blunder   | None        | 212, 213    | 252           | blunder     | After finished game, **blunder** will show the bad moves the client did.|
| timeline  | num         | 214         | 252, 260, 261 | represantation, image | After finished game.**timeline** display the **num** move of the game.|
| step      | None        | 214         | 252, 261      | represantation, image | After finished game. Step to next **timeline** index.|
| unstep    | None        | 214         | 252, 261      | represantation, image | After finished game. Step to bevore **timeline** index.|
| games     | None        | 215         | 52, 253       | game_name   | Will list all available games for the current lobby.|
| create    | game, mode, difficulty|200| 52, 254, 265  | None        | Will initialise a **game_config** and start the game.|
| evaluate  | game, difficulty, num | 201, 203 | 254, 262, 263 | wins, losses, draws |Will play up to **num** [max=100] games in a row and returns the evaluatuin stats.|
| stop_evaluate | None    | 203         | 252           | wins, losses, draws | Will stop a active Evaluation and returns evaluation stats

### Parameter difficulty:
| difficulty | MCTS dept |
| ---------- | --------- |
| easy       | 2         |
| medium     | 10        |
| hard       | 50        |
### Parameter mode:
  - player_vs_player
  - player_vs_ai
  - playerai_vs_ai
  - playerai_vs_playerai
### Paramter games:
  - Connect4
  - Othello
  - TicTacToe

# Debug Commands
| key       | Parameter   | Success code| Error code    | Return      | Discription |
|-----------|-------------|-------------|---------------|-------------|-------------|
| active_container | None | 300         | None          | count       | Will return every active container and the total container count. [Docker container ls] |
|game_client| None        | 301         | None          | debug       | Will aktivate debug mode of every new GameClient. GameClient will not be deleted.|

# Examples
## Lobby:
```json
{"command": "lobby", "command_key": "create", "key": "lobby_key"}
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