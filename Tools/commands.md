## Language Change Codes
- **LANGUAGECHANGED = <span style="color:lightgreen">0</span>** - Language changed successfully.
- **INVALIDLANGUAGE = <span style="color:lightgreen">1</span>** - Selected language not found.

## General Error Codes
- **INVALIDJSON = <span style="color:lightgreen">51</span>** - The received message is not a valid JSON
- **COMMANDNOTFOUND = <span style="color:lightgreen">52</span>** - The specified command does not exist
- **INVALIDGAME = <span style="color:lightgreen">53</span>** - The specified game does not exist
- **INVALIDDIFFICULTY = <span style="color:lightgreen">54</span>** - The specified difficulty level does not exist
- **INVALIDMODE = <span style="color:lightgreen">55</span>** - The specified game mode does not exist

## Lobby Success Codes
- **L_CREATED = <span style="color:lightgreen">100</span>** - Lobby has been successfully created
- **L_JOINED = <span style="color:lightgreen">101</span>** - Player has successfully joined the lobby
- **L_LEFT = <span style="color:lightgreen">102</span>** - Player has successfully left the lobby
- **L_SWAPPED = <span style="color:lightgreen">103</span>** - Player has successfully swapped positions within the lobby
- **L_POS = <span style="color:lightgreen">104</span>** - Current position in the lobby has been successfully retrieved
- **L_STATUS = <span style="color:lightgreen">105</span>** - Lobby status has been successfully retrieved
- **L_GAMES = <span style="color:lightgreen">106</span>** - List of games has been successfully retrieved

## Lobby Error Codes
- **L_CLIENTALREADYINLOBBY = <span style="color:lightgreen">150</span>** - Client is already in a lobby and cannot join multiple lobbies
- **L_LOBBYNOTEXIST = <span style="color:lightgreen">151</span>** - The specified lobby does not exist
- **L_JOINFAILURE = <span style="color:lightgreen">152</span>** - Failed to join the lobby
- **L_CLIENTNOTINLOBBY = <span style="color:lightgreen">153</span>** - The specified client is not in the lobby
- **L_POSUNKNOWN = <span style="color:lightgreen">154</span>** - The position within the lobby is unknown
- **L_POSOCCUPIED = <span style="color:lightgreen">155</span>** - The position within the lobby is already occupied
- **L_LOBBYNOTREADY = <span style="color:lightgreen">157</span>** - Lobby does not have enough players to start
- **L_NOLEAVEACTIVPLAYER = <span style="color:lightgreen">158</span>** - Client cannot leave an active game as a player
- **L_NOSWAP = <span style="color:lightgreen">159</span>** - Client cannot swap positions in an active game as a player
- **L_RUNNINGNOJOIN = <span style="color:lightgreen">160</span>** - Lobby is already running; join only as a spectator

## Play Success Codes
- **P_ARENAINIT = <span style="color:lightgreen">200</span>** - Arena has been successfully initialized
- **P_GAMEOVER = <span style="color:lightgreen">202</span>** - Game has ended successfully
- **P_VALIDMOVE = <span style="color:lightgreen">207</span>** - A valid move has been made
- **P_MOVES = <span style="color:lightgreen">208</span>** - List of possible moves has been successfully retrieved
- **P_VALIDUNDO = <span style="color:lightgreen">209</span>** - A valid undo action has been performed
- **P_SURRENDER = <span style="color:lightgreen">210</span>** - A player has surrendered successfully
- **P_BLUNDERLIST = <span style="color:lightgreen">212</span>** - List of blunders has been successfully retrieved
- **P_TIMELINE = <span style="color:lightgreen">214</span>** - Timeline of events in the game has been successfully retrieved
- **P_NOVALIDMOVES = <span style="color:lightgreen">215</span>** - Player does not have any valid moves left
- **P_STEP = <span style="color:lightgreen">216</span>** - Step forward in the timeline
- **P_UNSTEP = <span style="color:lightgreen">217</span>** - Step backward in the timeline
- **P_PLAYER = <span style="color:lightgreen">218</span>** - Sends the current active player
- **P_KIM = <span style="color:lightgreen">219</span>** - Send message if KIM is at turn
- **P_CREATEBLUNDER = <span style="color:lightgreen">220</span>** - Creating blunder for last game... taking some time.

## Play Error Codes
- **P_NOGAMECLIENT = <span style="color:lightgreen">250</span>** - No game client available; try again
- **P_NOPERMISSION = <span style="color:lightgreen">251</span>** - Player does not have permission to perform the action
- **P_NOTRUNNING = <span style="color:lightgreen">252</span>** - Game has not been initialized
- **P_ARGS = <span style="color:lightgreen">253</span>** - Invalid arguments provided
- **P_STILLRUNNING = <span style="color:lightgreen">254</span>** - Game is still running; requested action cannot be performed
- **P_NOMOVE = <span style="color:lightgreen">255</span>** - No move has been made
- **P_INVALIDMOVE = <span style="color:lightgreen">256</span>** - The move made is invalid
- **P_NOUNDO = <span style="color:lightgreen">258</span>** - No undo action available
- **P_INVALIDUNDO = <span style="color:lightgreen">259</span>** - The undo action attempted is invalid
- **P_NOTIMELINE = <span style="color:lightgreen">260</span>** - No timeline available
- **P_INVALIDTIMELINE = <span style="color:lightgreen">261</span>** - The specified timeline is invalid
- **P_NOGAMEINIT = <span style="color:lightgreen">266</span>** - Create a game first
- **P_NOTYOURTURN = <span style="color:lightgreen">268</span>** - Player tried to make a move out of turn
- **P_NOBLUNDER = <span style="color:lightgreen">269</span>** - Nothing in history to define blunder
- **P_BLUNDER = <span style="color:lightgreen">270</span>** - Server is working on blunder, please wait!

## Debug Codes
- **D_CONTAINER = <span style="color:lightgreen">300</span>** - List all active containers
- **D_TOGGLECLIENT = <span style="color:lightgreen">301</span>** - Toggle debug mode of the game client

---
# Available JSON Keys
- **command:** `debug`, `lobby`, `play`, `client`
- **command_key:** `create`, `valid_moves`, `make_move`, `undo_move`, `surrender`, `new_game`, `blunder`, `timeline`, `step`, `unstep`, `games`
- **data:** `pos`, `key`, `mode`, `game`, `difficulty`, `num`, `move`, `lang`

---
# Debug Module
| command | command_key      | Parameter | Success code | Error code | Return      | Discription                                                                                |
|---------|------------------|-----------|--------------|------------|-------------|--------------------------------------------------------------------------------------------|
| debug   | active_container | None      | 300          | None       | dict        | Will return every active container and the total container count. [Docker container ls]    |
| debug   | game_client      | None      | 301          | None       | debug       | Will activate debug mode of every new GameClient. GameClient will not be deleted on crash! |
| debug   | _                | None      | None         | 52         | command_key | Return a Error message if command_key is unknown to server!                                |

---
# Lobby Module
| command | command_key | Parameter  | Success code    | Error code         | Return                                           | Description                                                                                                                                     |
|---------|-------------|------------|-----------------|--------------------|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| lobby   | create      | None       | 100             | 150                | key                                              | Will create new lobby and sends key of lobby back. Client join directly as "p1". Clients can not create multiple lobby if there are in a lobby. |
| lobby   | join        | key, [pos] | 101 (Broadcast) | 150, 151, 160      | None                                             | Join lobby with **key** on - **Pos**                                                                                                            |
| lobby   | leave       | None       | 102 (Broadcast) | 153, 158           | None                                             | Leave a lobby.                                                                                                                                  |
| lobby   | swap        | pos        | 103 (Broadcast) | 153, 154, 155, 159 | None                                             | Change position in lobby to - **Pos** if not occupied or playing. [p1, p2, sp]                                                                  |
| lobby   | pos         | None       | 104             | 153                | pos                                              | Returns the current position of client if he is in a lobby.                                                                                     |
| lobby   | status      | None       | 105             | 153                | P1, P2, Spectators, GameClient, GameRunning, key | Returns the current state of the lobby the client is currently in.                                                                              |
| lobby   | games       | None       | 106             | 153                | games                                            | Returns a list of possible to play games as strings                                                                                             |
| lobby   | _           | None       | None            | 52                 | command_key                                      | Return a Error message if command_key is unknown to server!                                                                                     |
- **Parameter** with "[ ]" is optional.
- **Broadcast:** Every in this lobby gets the same response message. 

---
# Play Module
| command | command_key | Parameter              | Success code    | Error code                               | Return                            | Discription                                                                                               |
|---------|-------------|------------------------|-----------------|------------------------------------------|-----------------------------------|-----------------------------------------------------------------------------------------------------------|
| play    | create      | game, mode, difficulty | 200             | 53, 54, 55, 153, 157, 250, 251, 253, 254 | game, mode, difficulty, available | Will initialise a **game_config** and start the game.                                                     |
| play    | surrender   | None                   | 210 (Broadcast) | 153, 250, 251, 252                       | result                            | Client surrender active game and a broadcast message get triggered. Result is the winning player.         |
| play    | valid_moves | None                   | 208             | 153, 250, 251, 252                       | moves                             | Returns a new image from game with highlighted positions of possible moves.                               |
| play    | make_move   | move                   | 207             | 153, 250, 251, 252, 255, 256, 268        | None                              | Make a move on current game. - **move** can be an int or an tuple'[int, int]'. Like '[from, to]' '[2, 3]' |
| play    | undo_move   | num                    | 209             | 153, 250, 251, 252, 258, 259             | num                               | Undo the last **num** moves.                                                                              |
| play    | new_game    | None                   | 200             | 53, 54, 55, 153, 157, 250, 251, 254, 266 | None                              | Will start a new Game with last set configuration.                                                        |
| play    | blunder     | None                   | 212, 220        | 153, 250, 251, 254, 269, 270             | blunder                           | After finished game, **blunder** will show the bad moves the client did.                                  |
| play    | timeline    | num                    | 214             | 153, 250, 251, 254, 260, 261             | num, current_player, it           | After finished game.**timeline** display the **num** move of the game.                                    |
| play    | step        | None                   | 216             | 153, 250, 251, 254                       | current_player, it, last_it       | After finished game. Step to next **timeline** index.                                                     |
| play    | unstep      | None                   | 217             | 153, 250, 251, 254                       | current_player, it, last_it       | After finished game. Step to bevore **timeline** index.                                                   |
| play    | _           | None                   | None            | 52, 153, 250, 251                        | command_key                       | Return a Error message if command_key is unknown to server!                                               |
- **Broadcast:** Every in this lobby gets the same response message. 

---
# Client Module
| command | command_key | Parameter | Success code | Error code | Return      | Discription                                                 |
|---------|-------------|-----------|--------------|------------|-------------|-------------------------------------------------------------|
| client  | language    | lang      | 0            | 1          | lang        | Change the language response of sever to client             |
| debug   | _           | None      | None         | 52         | command_key | Return a Error message if command_key is unknown to server! |

---
# Game Configuration
## Parameter: Difficulty
| Difficulty | MCTS Depth |
|------------|------------|
| easy       | 35         |
| medium     | 75         |
| hard       | 150        |

## Parameter: Mode
- **Player vs Player mode**: `player_vs_player = 0`
- **Player vs Kim (an AI or specific character) mode**: `player_vs_kim = 1`
- **Kim vs Player mode (Kim starts or is in control first)**: `kim_vs_player = 2`
- **AI Player vs AI Player mode**: `playerai_vs_playerai = 3`
- **AI Player vs Kim mode**: `playerai_vs_kim = 4`
- **Kim vs AI Player mode**: `kim_vs_playerai = 5`

## Parameter: Games
- **Connect4**
  - A two-player connection game in which the players take turns dropping colored discs into a seven-column, six-row grid. The objective is to be the first to form a horizontal, vertical, or diagonal line of four discs.
- **Othello**
  - Also known as Reversi, this two-player strategy board game involves players taking turns placing discs on the board with their assigned color facing up. The goal is to have the majority of discs turned to display your color when the last playable empty square is filled.
- **TicTacToe**
  - A simple two-player game played on a 3x3 grid where players take turns marking a space with an X or O. The first player to align three of their marks horizontally, vertically, or diagonally wins the game.
- **Checkers**
  - A classic board game for two players, played on an 8x8 board with alternating colored squares. Each player starts with 12 pieces, and the objective is to capture all of the opponent's pieces or block them so they cannot move.
- **Nim**
  - A mathematical game of strategy where two players take turns removing objects from distinct heaps. On each turn, a player must remove at least one object, and the player forced to remove the last object loses.

---

## Available Languages
- **EN** English
  - The most widely spoken language in the world, primarily used in the United Kingdom, the United States, and many other countries.
- **DE** Deutsch
  - The official language of Germany, Austria, and parts of Switzerland, known for its rich literary and philosophical traditions.
- **FR** Français
  - The official language of France and many African countries, renowned for its influence on art, cuisine, and diplomacy.
- **ES** Español
  - The second most spoken language in the world, primarily used in Spain and Latin America, celebrated for its vibrant culture and history.


---
# Examples
## Lobby Module:
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
```json
{"command": "lobby", "command_key": "games"}
```
## Play Module:
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
## Debug Module
```json
{"command": "debug", "command_key": "active_container"}
```
```json
{"command": "debug", "command_key": "game_client"}
```
## Client Module
```json
{"command": "client", "command_key": "language", "lang":  "en"}
```