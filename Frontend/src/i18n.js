import { createI18n } from "vue-i18n";

const messages = {
  ////////////////////////////////////////////////English///////////////////////////////////////////////////////////////////////////////
  en: {
    message: {
      home: "Home",
      instruction: "Instruction",
      leaderboard: "Leaderboard",
      achievements: "Achievements",
      welcome: "Welcome to KIMaster",
      subtitle: "Here you can test your Game-AI",
      enter_lobby_key: "Enter Lobby Key",
      join_lobby: "Join Lobby",
      joinAs: "Join as",
      lobby_join_failed: "Lobby Join Failed!",
      lobby_swap_failed: "Position occupied!",
      game_start_failed: "Wrong amount of players!",
      createLobby: "Create Lobby",
      create: "Create",
      chess: "Chess",
      connect4: "Connect 4",
      tictactoe: "Tic Tac Toe",
      othello: "Othello",
      nim: "Nim",
      checkers: "Checkers",
      lobby: "Lobby",
      lobby_welcome: "Welcome to the",
      leave_lobby: "Leave Lobby",
      start_game: "Start Game",
      lobby_key_generating: "Lobby Key: Being Generated",
      lobby_key: "Lobby Key: {key}",
      your_position: "Your Position {position}",
      lobby_position:
        "Lobby Positions: P1= {p1} P2= {p2} Spectator {spectators}",
      lobbyPos: "Lobby Pos",
      lobbyStatus: "Lobby Status",
      webSocketConnectionStatus: "WebSocket Connection Status:",
      player1: "Player 1",
      player2: "Player 2",
      spectator: "Spectator",
      timeLine: "Timeline",
      player_vs_player: "Player vs Player",
      player_vs_ai: "Player vs KIM",
      playerai_vs_ai: "Player AI vs KIM",
      playerai_vs_playerai: "Player AI vs Player AI",
      KIM_vs_Player: "KIM vs Player",
      KIM_vs_Player_AI: "KIM vs Player AI",
      easy: "Easy",
      medium: "Medium",
      hard: "Hard",
      surrender: "Surrender",
      quit_game: "Quit Game",
      first: "First",
      previous: "Previous",
      next: "Next",
      last: "Last",
      undo_move: "Undo Move",
      new_game: "New Game",
      game_over: "Game Over",
      nim_move: "Make Move",
      row: "Row",
      amount: "Amount",
      player_1_won: "Player 1 Won",
      player_2_won: "Player 2 Won",
      game_over_after: "Game over after",
      turn: "Turn",
      turns: "Turns",
      okay: "Okay",
      show_rules: "Rules",
      return_to_game: "Return to Game",
      surrender_before_start:
        "You need to first surrender before you can start a new Game or Lobby",
      draw: "Draw!",
      startGame: "Start Game",
      waitMessage: "Waiting until Lobby is created...",
      connection_not_possible: "Connecting to Server wasn't possible",
      copyright: "© 2024 Your Company. All rights reserved.",
      step: "Step",
      unstep: "Undo step",
      evaluate: "Evaluate",
      valid_Moves_Instead: "Valid Moves Instead of Make Move",
      activateTwoTurnGame: "Activate two turn Game",
      undo_this_num_of_terms: "Undo this Number of turns",
      grid_Width: "Grid Width",
      grid_Height: "Grid Height",
      play: "Play",
      received_from_server: "Received From Server",
      command: "Command",
      command_key: "Command Key",
      key_value_pair_input: "Key-Value Pair Input",
      key: "Key",
      value: "Value",
      add_pair: "Add Pair",
      json_output: "JSON Output",
      your_turn: "Your Turn",
      opponent_turn: "Opponents Turn",
      blunder: "Show Blunders",
      you_won: "You Won!",
      opponent_won: "Opponent Won",
    },

    rules: {
      connect4: {
        game_title: "Connect4 Rules",
        description:
          "Connect 4 is a two-player game where players take turns dropping their colored disc into a column. The objective is to be the first to get four of your discs in a row, either horizontally, vertically, or diagonally.",

        setup: {
          title: "Setup",
          point1: "The game board consists of 7 columns and 6 rows.",
          point2:
            "Each player chooses a color and receives an unlimited number of discs of that color.",
        },
        gameplay: {
          title: "Gameplay",
          point1: "Players take turns dropping a disc into one of the columns.",
          point2:
            "The disc falls to the lowest available position within the column.",
          point3:
            "The game continues until a player gets four of their discs in a row or the board is full.",
        },
        endgame: {
          title: "Endgame",
          point1:
            "A player wins by getting four discs in a row (horizontally, vertically, or diagonally).",
          point2:
            "The game ends in a draw if the board is full and no player has four discs in a row.",
        },
      },

      tictactoe: {
        game_title: "Tic Tac Toe Rules",
        description:
          "Tic Tac Toe is a two-player game where players take turns marking a space in a 3x3 grid. The objective is to be the first to get three of your marks in a row, either horizontally, vertically, or diagonally.",

        setup: {
          title: "Setup",
          point1: "The game board consists of a 3x3 grid.",
          point2: "Each player chooses a mark, either 'X' or 'O'.",
        },
        gameplay: {
          title: "Gameplay",
          point1: "Players take turns marking a space in the grid.",
          point2:
            "The game continues until a player gets three of their marks in a row or all spaces are filled.",
        },
        endgame: {
          title: "Endgame",
          point1:
            "A player wins by getting three marks in a row (horizontally, vertically, or diagonally).",
          point2:
            "The game ends in a draw if all spaces are filled and no player has three marks in a row.",
        },
      },

      nim: {
        game_title: "Nim Rules",
        description:
          "Nim is a strategy game where players take turns removing stones from distinct heaps. The player who removes the last stone wins.",

        setup: {
          title: "Setup",
          point1: "There are several rows of stones",
          point2: "Two player take turns",
        },

        gameplay: {
          title: "Gameplay",
          point1: "Players take turns removing stones from a single row.",
          point2: "A player must take at least one stone on their turn.",
          point3: "A player may take multiple stones from the same row.",
          point4:
            "Players cannot take stones from more than one row in a single turn.",
        },

        endgame: {
          title: "Endgame",
          point1: "The player who takes the last stone wins.",
        },
      },

      othello: {
        game_title: "Othello Rules",
        description:
          "Othello is played by two players on an 8×8 board with round disks that are black on one side and white on the other. Each player is provided with several disks.",

        setup: {
          title: "Setup",
          point1: "The game is played on an 8×8 board.",
          point2:
            "Each player is given a number of disks with a black and a white side.",
          point3:
            "At the start of the game, four disks are placed in a predetermined position in the center of the board.",
        },
        gameplay: {
          title: "Gameplay",
          point1: "Player 'Black' always moves first.",
          point2:
            "A player must place a disk on an empty square adjacent to an opponent's disk, with at least one opponent's disk between the placed disk and another disk of the player's color.",
          point3:
            "After placing a disk, all opponent's disks in a straight line between the new disk and another disk of the player's color are flipped.",
          point4:
            "Players alternate turns. If a player cannot make a move that flips an opponent's disk, they must pass.",
        },
        endgame: {
          title: "Endgame",
          point1:
            "The game ends when the board is full or neither player can make a valid move.",
          point2:
            "The player with the most disks of their color on the board at the end wins.",
        },
      },

      checkers: {
        game_title: "Checkers Rules",
        description:
          "Checkers, also known as Draughts, is a strategy board game for two players. Each player starts with 12 pieces placed on the dark squares of the three rows closest to them. The objective of the game is to capture all of the opponent's pieces or block them so they cannot move.",

        setup: {
          title: "The Game Board at the Beginning",
          description:
            "The checkerboard is automatically placed so that a dark square is on the bottom left. The player with the white pieces starts.",
        },

        movement: {
          title: "Moving the Pieces",
          description:
            "Pieces move one square diagonally forward to an empty dark square.",
        },

        capturing: {
          title: "Capturing",
          description1: "There is a capture obligation. If your own free pieces cannot be clicked during a move, it may be because there is a capture opportunity somewhere on the board. Only one of these pieces can then be selected. Single pieces are only allowed to capture forward. When capturing, the piece must stand directly in front of the opponent's piece and must land directly behind the captured piece. This square must be free.",
          description2: "If you have a choice between different capture opportunities, you are free to decide. An exception is multiple captures.",
          description3: "Multiple captures mean: If a piece has captured and there is an opportunity to capture again with the same piece, the player continues their turn until multiple captures are no longer possible.",
        },

        queening: {
          title: "Queening",
          description1: "You get a queen when one of your pieces reaches the opponent's back row, either by a normal move or by a capture. The piece is marked with a 'Crown' (in the board game, a second piece is placed on top).",
          description2: "A queen can move diagonally both forward and backward and can also capture in both directions. Unlike international checkers, the king can only move one square forward or backward.",
        },

        endgame: {
          title: "End of the Game",
          description: "You lose if you have no pieces left or if your pieces are blocked and cannot move. You can also concede the game by choosing 'Surrender'.",
        },

        draw: {
          title: "Draw",
          description: "Some games end in a draw. This happens when neither player can win unless the other makes a significant mistake. To prevent endless games, there are two ways to declare a draw:",
          point1: "Both players agree to a draw, or",
          point2: "30 moves have been made without a capture.",
        },
      },
    },

    instructions: {
      instruction_title: "Instructions",
      introduction: {
        title: "Introduction",
        description1: "This documentation describes the process of using a WebSocket connection in a selected programming language to connect to the URI wss://kimaster.mni.thm.de/ws.",
        description2: "Additionally, it explains how to log in to the THM internal network and send messages in JSON format and receive feedback from the server.",
        description3: "A sample connection using Python is also provided.",
      },
      requirements: {
        title: "Requirements",
        network_access: "You must be in the THM internal network. This can be done either via the THM VPN or the Eduroam network.",
        websocket_uri_title: "WebSocket URI: ",
        websocket_uri: "wss://kimaster.mni.thm.de/ws",
        browser_url_title: "Browser URL:",
        browser_url: " https://kimaster.mni.thm.de (for browser connections)",
        message_format_title: "Message format: ",
        message_format: "JSON",
        documentation_title: "Documentation: ",
        documentation: "Information about the JSON commands can be found in the command.md file."
      },
      webSocketConnection: {
        title: "WebSocket Connection",
        step1: {
          title: "Step 1: Establish Network Access",
          vpn: "THM VPN:",
          vpn_description: " Connect to the THM VPN. You can find instructions on how to set it up on the official THM website.",
          vpn_link: "THM VPN Guide",
          eduroam:"Eduroam Network: ",
          eduroam_description: "Alternatively, you can connect to the Eduroam network, if available.",
          eduroam_link: "Eduroam Guide"
        },
        step2: {
          title: "Step 2: Establish WebSocket Connection",
          browser: {
            title: "Connection via Browser",
            open_browser: "1. Open your web browser.",
            enter_url: "2. Enter the URL https://kimaster.mni.thm.de.",
            internal_network: "3. Ensure you are in the THM internal network.",
          },
          connection_with_ProgrammingLanguage: {
            title: "Connection with a Programming Language (Python Example)",
            install_python:"1. Install Python: Ensure Python is installed on your computer.",
            install_webSocket:"2. Install WebSocket library: Install the WebSocket library for Python using the following command:",
            pip_command: "pip install websocket-client",
            connection_code: "Connection code:",
            example_code: `
          import asyncio
          import json
          from abc import ABC
          import io
          from typing import Coroutine
          from PIL import Image
          from websockets import WebSocketClientProtocol, connect, InvalidURI, ConnectionClosedOK
          
          class KIMaster(ABC):
              def __init__(self, uri_pool: list[str]):
                  """
                  Initialize the KIMaster with a list of URIs.
                  :param uri_pool: List of URIs to connect to.
                  """
                  self.connection: WebSocketClientProtocol | None = None
                  self.uri_pool: list[str] = uri_pool
          
              async def connect(self) -> None:
                  """
                  Try to connect to one of the URIs in the uri_pool.
                  """
                  for uri in self.uri_pool:
                      print(f"Try to connect to URI: '{uri}'")
                      try:
                          self.connection = await connect(uri)
                          print(f"Connected to URI: '{uri}'")
                          break
                      except InvalidURI:
                          print(f"URI: '{uri}' not reachable!")
          
              async def send_cmd(self, command: str, command_key: str, data: dict | None = None) -> None:
                  """
                  Send a command to the connected WebSocket server.
                  :param command: The command to send.
                  :param command_key: The command key associated with the command.
                  :param data: Optional additional data to send with the command.
                  """
                  if self.connection:
                      payload: dict = {"command": command, "command_key": command_key}
                      if data is not None:
                          payload.update(data)
                      await self.connection.send(json.dumps(payload))
          
              async def receive(self) -> dict | str | bytes | None:
                  """
                  Receive a message from the WebSocket server.
                  :return: The received message, either as a dictionary, string, or bytes.
                  """
                  if self.connection:
                      message = None
                      try:
                          message = await self.connection.recv()
                      except ConnectionClosedOK:
                          return
                      try:
                          data = json.loads(message)
                          return data
                      except json.JSONDecodeError:
                          return message
                      except UnicodeDecodeError:
                          return message
          
              async def close(self) -> None:
                  """
                  Close the WebSocket connection.
                  """
                  if self.connection:
                      await self.connection.close()
          
              def run(self, target: Coroutine) -> None:
                  """
                  Run the given coroutine until it completes.
                  :param target: The coroutine to run.
                  """
                  asyncio.run(target)
          
              async def handler(self, send_handler, receive_handler) -> None:
                  """
                  Handle both sending and receiving of WebSocket messages.
                  :param send_handler: The coroutine handling sending messages.
                  :param receive_handler: The coroutine handling receiving messages.
                  """
                  send_task = asyncio.create_task(send_handler())
                  receive_task = asyncio.create_task(receive_handler())
                  await asyncio.gather(send_task, receive_task)
          
              def print_message(self, message: dict) -> None:
                  """
                  Print a formatted message to the console.
                  :param message: The message to print.
                  """
                  print("\\n")
                  for k, v in message.items():
                      print(f" -- {k}: {v}")
          
              def show(self, message: bytes) -> None:
                  """
                  Display an image from a byte stream.
                  :param message: The image data as bytes.
                  """
                  image_stream = io.BytesIO(message)
                  image = Image.open(image_stream)
                  image.show()
          `,
          }
        },
        step3: {
          title: "Step 3: Send JSON Messages",
          json_format: "1. Format JSON message: ",
          json_format_description: "All messages must be sent in JSON format.",
          example_message: "2. Example message:",
          example_code: `
            {
              "command": "start_game",
              "parameters": {}
            }
          `,
          send_message: "3. Send message:",
          send_message_description: "Use the WebSocket library of your chosen programming language to send messages.",
        },
        step4: {
          title: "Step 4: Receive Feedback",
          json_feedback: "1. JSON feedback: ",
          feedback: "The server sends feedback in JSON format.",
          bytestream: "2. Receive bytestreams: ",
          bytestream_receive: "If the feedback is a bytestream representing a PNG, save it accordingly.",
        },
      },
    },
    footer: {
      datenschutz: 'Privacy Policy',
      impressum: 'Imprint'
    },
  },

  ////////////////////////////////////////////////////German/////////////////////////////////////////////////////////////////////////////////////////
  de: {
    message: {
      home: "Startseite",
      instruction: "Anleitung",
      leaderboard: "Rangliste",
      achievements: "Erfolge",
      welcome: "Willkommen zu KIMaster",
      subtitle: "Hier kannst du deine Spiele-KI testen",
      enter_lobby_key: "Lobby-Schlüssel eingeben",
      join_lobby: "Lobby beitreten",
      joinAs: "Beitreten als",
      lobby_join_failed: "Lobbybeitritt fehlgeschlagen!",
      lobby_swap_failed:"Position besetzt!",
      game_start_failed: "Falsche Spieleranzahl!",
      createLobby: "Lobby erstellen",
      create: "erstellen",
      chess: "Schach",
      connect4: "Vier Gewinnt",
      tictactoe: "Tic Tac Toe",
      othello: "Othello",
      nim: "Nim",
      checkers: "Dame",
      lobby: "Lobby",
      lobby_welcome: "Willkommen zur {game}",
      leave_lobby: "Lobby verlassen",
      start_game: "Spiel starten",
      lobby_key_generating: "Lobby-Schlüssel: Wird generiert",
      lobby_key: "Lobby-Schlüssel: {key}",
      your_position: "Ihre Position {position}",
      lobby_position: "Lobby Positionen: P1= {p1} P2= {p2} Zuschauer {spectators}",
      lobbyPos: "Lobby Pos",
      lobbyStatus: "Lobby Status",
      webSocketConnectionStatus: "WebSocketverbindung Status:",
      player1: "Spieler 1",
      player2: "Spieler 2",
      spectator: "Zuschauer",
      timeLine: "Zeitleiste",
      player_vs_player: "Spieler gegen Spieler",
      player_vs_ai: "Spieler gegen KIM",
      playerai_vs_ai: "Spieler-KI gegen KIM",
      playerai_vs_playerai: "Spieler-KI gegen Spieler-KI",
      KIM_vs_Player: "KIM gegen Spieler",
      KIM_vs_Player_AI: "KIM gegen Spieler KI",
      easy: "Einfach",
      medium: "Mittel",
      hard: "Schwer",
      surrender: "Aufgeben",
      quit_game: "Spiel verlassen",
      first: "Erstes",
      previous: "Vorherig",
      next: "Nächstes",
      last: "Letztes",
      undo_move: "Zug zurück",
      new_game: "Neues Spiel",
      game_over: "Spiel vorbei",
      nim_move: "Zug ausführen",
      row: "Reihe",
      amount: "Anzahl",
      player_1_won: "Spieler 1 hat gewonnen",
      player_2_won: "Spieler 2 hat gewonnen",
      game_over_after: "Spiel vorbei nach",
      turn: "Zug",
      turns: "Zügen",
      okay: "Okay",
      show_rules: "Regeln",
      return_to_game: "Zurück zum Spiel",
      surrender_before_start:
        "Sie müssen erst aufgeben, bevor Sie ein neues Spiel oder eine neue Lobby beginnen können",
      draw: "Unentschieden!",
      startGame: "Spiel Starten",
      waitMessage: "Warten, bis die Lobby erstellt ist...",
      connection_not_possible: "Die Verbindung zum Server war nicht möglich",
      copyright: "© 2024 Dein Unternehmen. Alle Rechte vorbehalten.",
      step: "Schritt",
      unstep: "Schritt rückgängig machen",
      evaluate: "bewerten",
      valid_Moves_Instead: "Gültige Züge anstelle von Zug machen",
      activateTwoTurnGame: "Aktivieren Sie zwei Runden Spiel",
      undo_this_num_of_terms: "Die Anzahl der Umdrehungen rückgängig machen",
      grid_Width: "Breite des Rasters",
      grid_Height: "Rasterhöhe",
      play: "Spielen",
      received_from_server: "Empfangen vom Server",
      command: "Befehl",
      command_key: "Befehlstaste",
      key_value_pair_input: "Schlüssel-Werte-Paar Eingabe",
      key: "Schlüssel",
      value: "Wert",
      add_pair: "Paar hinzufügen",
      json_output: "JSON-Ausgabe",
      your_turn: "Dein Zug",
      opponent_turn: "Gegner am Zug",
      blunder: "Fehler anzeigen",
      you_won: "Du hast gewonnen!",
      opponent_won: "Gegner hat gewonnen",
    },
/////////////////////////////////////////Spielregeln///////////////////////////////////////////////////////////////////////////////////////
    rules: {
      connect4: {
        game_title: "Vier Gewinnt Regeln",
        description:
          " Vier Gewinnt ist ein Zwei-Personen-Spiel, bei dem die Spieler abwechselnd einen Stein ihrer Farbe in eine der sieben Spalten des Gitters fallen lassen. Das Ziel ist es, als Erster vier Steine in einer Reihe zu haben, sei es horizontal, vertikal oder diagonal.",

        setup: {
          title: "Spielvorbereitung",
          point1: "Das Spielbrett besteht aus 7 Spalten und 6 Reihen",
          point2:
            "Jeder Spieler wählt eine Farbe und erhält eine unbegrenzte Anzahl an Steinen in dieser Farbe.",
        },
        gameplay: {
          title: "Spielablauf",
          point1:
            "Die Spieler lassen abwechselnd einen Stein in eine der Spalten fallen.",
          point2:
            "Der Stein fällt in die tiefste verfügbare Position in der Spalte.",
          point3:
            "Das Spiel geht weiter, bis ein Spieler vier seiner Steine in einer Reihe hat oder das Spielfeld voll ist.",
        },
        endgame: {
          title: "Spielende",
          point1:
            "Ein Spieler gewinnt, wenn er vier Steine in einer Reihe hat (horizontal, vertikal oder diagonal).",
          point2:
            "Das Spiel endet unentschieden, wenn das Spielfeld voll ist und kein Spieler vier Steine in einer Reihe hat.",
        },
      },

      tictactoe: {
        game_title: "Tic Tac Toe Regeln",
        description:
          "Tic Tac Toe ist ein Zwei-Personen-Spiel, bei dem die Spieler abwechselnd ein Feld in einem 3x3 Raster markieren. Das Ziel ist es, als Erster drei seiner Zeichen in einer Reihe zu haben, sei es horizontal, vertikal oder diagonal.",

        setup: {
          title: "Spielvorbereitung",
          point1: "Das Spielfeld besteht aus einem 3x3 Raster.",
          point2: 'Jeder Spieler wählt ein Zeichen, entweder "X" oder "O".',
        },

        gameplay: {
          title: "Spielablauf",
          point1: "Die Spieler markieren abwechselnd ein Feld im Raster.",
          point2:
            "Das Spiel geht weiter, bis ein Spieler drei seiner Zeichen in einer Reihe hat oder alle Felder belegt sind.",
        },

        endgame: {
          title: "Spielende",
          point1:
            "Ein Spieler gewinnt, wenn er drei Zeichen in einer Reihe hat (horizontal, vertikal oder diagonal).",
          point2:
            "Das Spiel endet unentschieden, wenn alle Felder belegt sind und kein Spieler drei Zeichen in einer Reihe hat.",
        },
      },

      nim: {
        game_title: "Nim Regeln",
        description:
          "Nim ist ein Strategiespiel, bei dem die Spieler abwechselnd Steine aus verschiedenen Reihen nehmen. Der Spieler, der den letzten Stein nimmt, gewinnt.",

        setup: {
          title: "Spielvorbereitung",
          point1: "Es gibt mehrere Reihen von Steinen.",
          point2: "Zwei Spieler sind an der Reihe.",
        },

        gameplay: {
          title: "Spielablauf",
          point1:
            "Die Spieler nehmen abwechselnd Steine aus einer einzigen Reihe.",
          point2:
            "Ein Spieler muss mindestens einen Stein in seinem Zug nehmen.",
          point3: "Ein Spieler kann mehrere Steine aus derselben Reihe nehmen.",
          point4:
            "Die Spieler können nicht Steine aus mehr als einer Reihe in einem Zug nehmen.",
        },

        endgame: {
          title: "Spielende",
          point1: "Der Spieler, der den letzten Stein nimmt, gewinnt.",
        },
      },

      othello: {
        game_title: "Othello Regeln",
        description:
          "Othello wird von zwei Spielern auf einem 8×8-Brett mit runden Steinen gespielt, die eine schwarze und eine weiße Seite haben. Jeder Spieler erhält mehrere Steine.",

        setup: {
          title: "Aufbau",
          point1: "Das Spiel wird auf einem 8×8-Brett gespielt.",
          point2:
            "Jeder Spieler erhält mehrere Steine mit einer schwarzen und einer weißen Seite.",
          point3:
            "Zu Beginn des Spiels werden vier Steine in einer vorgegebenen Position in der Mitte des Brettes platziert.",
        },
        gameplay: {
          title: "Spielablauf",
          point1: "Spieler 'Schwarz' macht immer den ersten Zug.",
          point2:
            "Ein Spieler muss einen Stein auf ein leeres Feld legen, das an ein Feld mit gegnerischen Steinen angrenzt, wobei mindestens ein gegnerischer Stein zwischen dem neuen und einem anderen Stein derselben Farbe liegen muss.",
          point3:
            "Nach dem Platzieren eines Steins werden alle gegnerischen Steine in einer geraden Linie zwischen dem neuen Stein und einem anderen Stein derselben Farbe umgedreht.",
          point4:
            "Die Spieler wechseln sich ab. Wenn ein Spieler keinen gültigen Zug machen kann, muss er passen.",
        },
        endgame: {
          title: "Spielende",
          point1:
            "Das Spiel endet, wenn das Brett voll ist oder beide Spieler keinen gültigen Zug mehr machen können.",
          point2:
            "Der Spieler mit den meisten Steinen seiner Farbe auf dem Brett am Ende gewinnt.",
        },
      },

      checkers: {
        game_title: "Dame Regeln",
        description:
          "Dame ist ein strategisches Brettspiel für zwei Spieler. Jeder Spieler beginnt mit 12 Steinen, die auf den dunklen Feldern der drei ihm nächstgelegenen Reihen platziert werden. Ziel des Spiels ist es, alle gegnerischen Steine zu schlagen oder zu blockieren, sodass sie nicht mehr ziehen können.",

        setup: {
          title: "Das Spielbrett zu Beginn",
          description:
            "Das Damebrett wird automatisch so platziert, dass links unten ein dunkles Feld liegt. Der Startspieler beginnt mit den weißen Steinen.",
        },

        movement: {
          title: "Das Ziehen der Steine",
          description:
            "Die Steine ziehen ein Feld in diagonaler Richtung, aber nur vorwärts und nur auf freie dunkle Felder.",
        },

        capturing: {
          title: "Schlagen",

          description1:
            "Es gilt Schlagzwang. Wenn sich eigene freie Steine bei einem Zug nicht anklicken lassen, kann das daran liegen, dass irgendwo auf dem Brett die Möglichkeit zum Schlagen besteht. Nur einer dieser Steine kann dann ausgewählt werden. Einfache Steine dürfen nur vorwärts schlagen. Beim Schlagen muss der Stein direkt vor dem gegnerischen Stein stehen und muss nach dem Schlagen direkt hinter dem geschlagenen Stein landen. Dieses Feld muss frei sein.",
          description2:
            "Wenn man die Auswahl zwischen verschiedenen Schlagmöglichkeiten hat, darf man frei entscheiden. Ausnahme bildet Mehrfachschlagen.",
          description3:
            "Mehrfachschlagen bedeutet: Wenn geschlagen wurde und danach die Möglichkeit besteht, noch einmal zu schlagen mit demselben Stein, so bleibt der Spieler am Zug, bis Mehrfachschlagen nicht länger möglich ist.",
        },

        queening: {
          title: "In Dame umwandeln",
          description1:
            "Man bekommt eine Dame, wenn einer der eigenen Steine auf der gegnerischen Grundlinie stehen bleibt, egal ob durch einen normalen Zug oder durch ein Schlagen. Der Stein wird dann durch eine 'Krone' gekennzeichnet (im Brettspiel wird ein zweiter Stein darauf gestellt).",
          description2:
            "Eine Dame kann nun sowohl schräg vorwärts als auch rückwärts bewegt werden und genauso darf man mit ihr auch schlagen. Im Gegensatz zur internationalen Damenvariante darf sich die Dame aber nur um ein Feld vorwärts oder rückwärts bewegen.",
        },

        endgame: {
          title: "Spielende",
          description:
            "Man hat verloren, wenn man keinen Stein mehr hat oder wenn man mit seinen Steinen keinen Zug mehr machen kann, weil die eigenen Steine durch den Gegner blockiert sind. Man kann auch die Partie verloren geben durch die Aktion 'Aufgeben', zum Beispiel weil man so weit zurück liegt, dass ein weiteres Spielen keinen Sinn mehr macht.",
        },

        draw: {
          title: "Unentschieden",
          description:
            "Manche Partien gehen unentschieden aus. In so einem Fall kann keiner der beiden Spieler mehr gewinnen, es sei denn, der andere macht einen enormen Fehler. Um endlose Partien zu vermeiden, gibt es zwei Möglichkeiten für ein Unentschieden:",
          point1: "Beide Spieler sind sich darin einig geworden, oder",
          point2:
            "30 Züge wurden gezogen, in denen kein Stein geschlagen wurde.",
        },
      },
    },
///////////////////////////////////////////////////////////////Anleitung/////////////////////////////////////////////////////////////////////////////////////////////////////
    instructions: {
      instruction_title: "Anmeldungsdokumentation",

      introduction: {
        title: "Einleitung",
        description1:
          "Diese Dokumentation beschreibt den Prozess zur Nutzung einer WebSocket-Verbindung in einer ausgewählten Programmiersprache, um eine Verbindung zu der URI wss://kimaster.mni.thm.de/ws herzustellen. ",
        description2:
          "Zusätzlich wird beschrieben, wie man sich im THM internen Netzwerk anmeldet und Nachrichten im JSON-Format sendet sowie Rückmeldungen vom Server empfängt.",
        description3:
          " Es wird auch eine Beispielsverbindung mit Python vorgestellt.",
      },

      requirements: {
        title: "Voraussetzungen",
        network_access:"Sie müssen sich im THM internen Netzwerk befinden. Dies kann entweder über das THM VPN oder das Eduroam Netzwerk erfolgen.",
        websocket_uri_title: "WebSocket-URI:",
        websocket_uri:" wss://kimaster.mni.thm.de/ws",
        browser_url_title:"Browser-URL:",
        browser_url: " https://kimaster.mni.thm.de (für Verbindungen über den Browser)",
        message_format_title: "Nachrichtenformat: ",
        message_format: "JSON",
        documentation_title: "Dokumentation:",
        documentation:"Informationen zu den JSON-Kommandos finden Sie in der Datei command.md"
      },

      webSocketConnection: {
        title: "Verbindung mit Websocket",
        step1: {
          title: "Schritt 1: Netzwerkzugang herstellen",
          vpn: "THM VPN:",
          vpn_description: " Verbinden Sie sich mit dem THM VPN. Anweisungen zur Einrichtung finden Sie auf der offiziellen THM-Website.",
          vpn_link: "THM VPN Anleitung",
          eduroam:"Eduroam Netzwerk: ",
          eduroam_description: "Alternativ können Sie sich mit dem Eduroam Netzwerk verbinden, falls verfügbar.",
          eduroam_link: "Eduroam Anleitung"
        },
        step2: {
          title: "Schritt 2: WebSocket-Verbindung herstellen",
          browser: {
            title: " Verbindung über Browser",
            open_browser: "1. Öffnen Sie Ihren Webbrowser.",
            enter_url: "2. Geben Sie die URL https://kimaster.mni.thm.de ein.",
            internal_network:"3. Stellen Sie sicher, dass Sie sich im THM internen Netzwerk befinden.",
          },
          connection_with_ProgrammingLanguage: {
            title:
              "Verbindung mit einer Programmiersprache (Beispiel in Python)",
            install_python:
              "1. Python installieren: Stellen Sie sicher, dass Python auf Ihrem Computer installiert ist.",
            install_webSocket:
              "2. WebSocket-Bibliothek installieren: Installieren Sie die WebSocket-Bibliothek für Python mit folgendem Befehl:",
            pip_command: "pip install websocket-client",
            connection_code: "Connection Code Beispiel:",
            sending_code: "Sending Code Beispiel",

            example_code: `
          
            import asyncio
            import json
            from abc import ABC
            import io
            from typing import Coroutine
            from PIL import Image
            from websockets import WebSocketClientProtocol, connect, InvalidURI, ConnectionClosedOK
            
            class KIMaster(ABC):
                def __init__(self, uri_pool: list[str]):
                    """
                    Initialize the KIMaster with a list of URIs.
                    :param uri_pool: List of URIs to connect to.
                    """
                    self.connection: WebSocketClientProtocol | None = None
                    self.uri_pool: list[str] = uri_pool
            
                async def connect(self) -> None:
                    """
                    Try to connect to one of the URIs in the uri_pool.
                    """
                    for uri in self.uri_pool:
                        print(f"Try to connect to URI: '{uri}'")
                        try:
                            self.connection = await connect(uri)
                            print(f"Connected to URI: '{uri}'")
                            break
                        except InvalidURI:
                            print(f"URI: '{uri}' not reachable!")
            
                async def send_cmd(self, command: str, command_key: str, data: dict | None = None) -> None:
                    """
                    Send a command to the connected WebSocket server.
                    :param command: The command to send.
                    :param command_key: The command key associated with the command.
                    :param data: Optional additional data to send with the command.
                    """
                    if self.connection:
                        payload: dict = {"command": command, "command_key": command_key}
                        if data is not None:
                            payload.update(data)
                        await self.connection.send(json.dumps(payload))
            
                async def receive(self) -> dict | str | bytes | None:
                    """
                    Receive a message from the WebSocket server.
                    :return: The received message, either as a dictionary, string, or bytes.
                    """
                    if self.connection:
                        message = None
                        try:
                            message = await self.connection.recv()
                        except ConnectionClosedOK:
                            return
                        try:
                            data = json.loads(message)
                            return data
                        except json.JSONDecodeError:
                            return message
                        except UnicodeDecodeError:
                            return message
            
                async def close(self) -> None:
                    """
                    Close the WebSocket connection.
                    """
                    if self.connection:
                        await self.connection.close()
            
                def run(self, target: Coroutine) -> None:
                    """
                    Run the given coroutine until it completes.
                    :param target: The coroutine to run.
                    """
                    asyncio.run(target)
            
                async def handler(self, send_handler, receive_handler) -> None:
                    """
                    Handle both sending and receiving of WebSocket messages.
                    :param send_handler: The coroutine handling sending messages.
                    :param receive_handler: The coroutine handling receiving messages.
                    """
                    send_task = asyncio.create_task(send_handler())
                    receive_task = asyncio.create_task(receive_handler())
                    await asyncio.gather(send_task, receive_task)
            
                def print_message(self, message: dict) -> None:
                    """
                    Print a formatted message to the console.
                    :param message: The message to print.
                    """
                    print("\\n")
                    for k, v in message.items():
                        print(f" -- {k}: {v}")
            
                def show(self, message: bytes) -> None:
                    """
                    Display an image from a byte stream.
                    :param message: The image data as bytes.
                    """
                    image_stream = io.BytesIO(message)
                    image = Image.open(image_stream)
                    image.show()
            
                    `,
          },
        },
        step3: {
          title: "Schritt 3: JSON-Nachrichten senden",
          json_format: "1. JSON-Nachricht formatieren: ",
          json_format_descripton:
            "Alle Nachrichten müssen im JSON-Format gesendet werden.",
          example_message: "2. Beispielnachricht:",
          example_code: {
            command: "start_game",
            parameters: {},
          },

          send_message: "3. Nachricht senden:",
          send_message_description:
            "Nutzen Sie die WebSocket-Bibliothek Ihrer gewählten Programmiersprache, um Nachrichten zu senden.",
        },

        step4: {
          title: "Schritt 4: Rückmeldung empfangen",
          json_feedback: " 1. JSON-Rückmeldungen:",
          feedback: "Der Server sendet Rückmeldungen im JSON-Format zurück.",
          bytestream: "2. Bytestreams empfangen:",
          bytestream_receive:
            "Falls die Rückmeldung ein Bytestream ist, der ein PNG darstellt, speichern Sie diesen entsprechend ab.",
        },
      },
    },
    footer: {
      datenschutz: 'Datenschutz',
      impressum: 'Impressum'
    },
  },
////////////////////////////////////////////////////////////////Französisch///////////////////////////////////////////////////////////////////////////////////
  fr: {
    message: {
      home: "Accueil",
      instruction: "Instruction",
      leaderboard: "Classement",
      achievements: "Réalisations",
      welcome: "Bienvenue chez KIMaster",
      subtitle: "Ici, vous pouvez tester votre IA de jeu",
      enter_lobby_key: "Entrez la clé de la salle",
      join_lobby: "Rejoindre la salle",
      lobby_join_failed: "Échec de la connexion à la salle!",
      lobby_swap_failed: "Position occupée!",
      game_start_failed: "Nombre de joueurs incorrect!",
      createLobby: "créer un hall d'entrée",
      create: "créer",
      joinAs: "Adhérer en tant que",
      chess: "Échecs",
      connect4: "Puissance 4",
      tictactoe: "Morpion",
      othello: "Othello",
      nim: "Nim",
      checkers: "Dame",
      leave_lobby: "Quitter la salle",
      start_game: "Commencer le jeu!",
      lobby_key_generating: "Clé de salle: Génération en cours",
      lobby_key: "Clé de salle: {key}",
      your_position: "Votre position {position}",
      lobby_position:
        "Positions du lobby: P1= {p1} P2= {p2} Spectateurs {spectators}",
      lobbyPos: "Lobby Pos",
      lobbyStatus: "Statut du lobby",
      webSocketConnectionStatus: "État de la connexion WebSocket:",
      player1: "Joueur 1",
      player2: "Joueur 2",
      spectator: "Spectateur",
      timeLine: "Ligne temporelle",
      player_vs_player: "Joueur contre Joueur",
      player_vs_ai: "Joueur contre KIM",
      playerai_vs_ai: "IA Joueur contre KIM",
      playerai_vs_playerai: "IA Joueur contre IA Joueur",
      KIM_vs_Player: "KIM contre les joueurs",
      KIM_vs_Player_AI: "KIM contre joueur IA",
      easy: "Facile",
      medium: "Moyen",
      hard: "Difficile",
      lobby: "Lobby",
      lobby_welcome: "Bienvenue dans la salle de {game}",
      surrender: "Abandonner",
      quit_game: "Quitter le jeu",
      first: "Premier",
      previous: "Précédent",
      next: "Suivant",
      last: "Dernier",
      undo_move: "Annuler le coup",
      new_game: "Nouveau jeu",
      game_over: "Fin du jeu",
      nim_move: "Faire move",
      row: "Rangée",
      amount: "Quantité",
      player_1_won: "Le joueur 1 a gagné",
      player_2_won: "Le joueur 2 a gagné",
      game_over_after: "Fin du jeu après",
      turn: "Tour",
      turns: "Tours",
      okay: "D'accord",
      show_rules: "réglementer",
      return_to_game: "Retour au jeu",
      surrender_before_start:
        "Vous devez abandonner avant de pouvoir commencer une nouvelle partie ou un nouveau lobby.",
      draw: "Match nul!",
      startGame: "Démarrer le jeu",
      waitMessage: "Attendre que le lobby soit créé...",
      connection_not_possible: "La connexion au serveur n'était pas possible",
      copyright: "© 2024 Votre entreprise. Tous droits réservés.",
      step: "étape",
      unstep: "annuler l'étape",
      evaluate: "évaluer",
      valid_Moves_Instead:
        "Des mouvements valables au lieu de faire un mouvement",
      activateTwoTurnGame: "Activer deux tours de jeu",
      undo_this_num_of_terms: "Annuler le nombre de rotations",
      grid_Width: "Largeur de la grille",
      grid_Height: "Hauteur de la grille",
      play: "Jouer",
      received_from_server: "Reçu du serveur",
      command: "Commandement",
      command_key: "Touche de commande",
      key_value_pair_input: "Entrée d'une paire clé-valeur",
      key: "Clé",
      value: "Valeur",
      add_pair: "Ajouter une paire",
      json_output: "Sortie JSON",
      your_turn: "Ton tour",
      opponent_turn: "Au tour de l'adversaire",
      blunder: "Montre Erreurs",
      you_won: "Vous avez gagné!",
      opponent_won: "L'adversaire a gagné",
    },
/////////////////////////////////////////////////////////////Spielregeln//////////////////////////////////////////////////////////////////////////////////////////////
    rules: {
      connect4: {
        game_title: 'Règles du jeu "Quatre gagnants',
        description:
          " Quatre gagnants est un jeu pour deux personnes dans lequel les joueurs font tomber à tour de rôle un pion de leur couleur dans l'une des sept colonnes de la grille. Le but est d'être le premier à aligner quatre pions, que ce soit horizontalement, verticalement ou en diagonale.",

        setup: {
          title: "Préparation du jeu",
          point1: "Le plateau de jeu se compose de 7 colonnes et 6 rangées",
          point2:
            "Chaque joueur choisit une couleur et reçoit un nombre illimité de pions de cette couleur.",
        },

        gameplay: {
          title: "Déroulement du jeu",
          point1: "Les joueurs marquent à tour de rôle une case de la grille.",
          point2:
            "La pierre tombe dans la position la plus basse disponible dans la colonne.",
          point3:
            "Le jeu se poursuit jusqu'à ce qu'un joueur ait aligné quatre de ses pions ou que le plateau de jeu soit plein.",
        },
        endgame: {
          title: "Fin du jeu",
          point1:
            "Un joueur gagne s'il a trois signes dans une rangée (horizontale, verticale ou diagonale).",
          point2:
            "Le jeu se termine par un match nul lorsque toutes les cases sont occupées et qu'aucun joueur n'a trois signes dans une rangée.",
        },
      },

      tictactoe: {
        game_title: "Règles du Tic Tac Toe",
        description:
          "Tic Tac Toe est un jeu à deux personnes dans lequel les joueurs marquent à tour de rôle une case dans une grille 3x3. Le but est d'être le premier à aligner trois de ses signes, que ce soit horizontalement, verticalement ou en diagonale.",

        setup: {
          title: "Préparation du jeu",
          point1: "Le terrain de jeu se compose d'une grille de 3x3.",
          point2: "Chaque joueur choisit un signe, soit 'X', soit 'O'.",
        },

        gameplay: {
          title: "Déroulement du jeu",
          point1: '"Les joueurs marquent à tour de rôle une case de la grille.',
          point2:
            "Le jeu se poursuit jusqu'à ce qu'un joueur ait aligné trois de ses signes ou que toutes les cases soient occupées.",
        },
        endgame: {
          title: "Fin du jeu",
          point1:
            "Un joueur gagne s'il a trois signes dans une rangée (horizontale, verticale ou diagonale).",
          point2:
            "Le jeu se termine par un match nul lorsque toutes les cases sont occupées et qu'aucun joueur n'a trois signes dans une rangée.",
        },
      },

      nim: {
        game_title: "Règles de Nim",
        description:
          "Nim est un jeu de stratégie où les joueurs prennent tour à tour des pierres dans des tas distincts. Le joueur qui enlève la dernière pierre gagne ou perd, selon la règle convenue.",
        setup: {
          title: "Préparation",
          point1: "Il y a plusieurs rangées de pierres.",
          point2: "Deux joueurs jouent à tour de rôle.",
        },
        gameplay: {
          title: "Déroulement du jeu",
          point1:
            "Les joueurs prennent à tour de rôle des pierres d'une seule rangée.",
          point2: "Un joueur doit prendre au moins une pierre à son tour.",
          point3: "Un joueur peut prendre plusieurs pierres de la même rangée.",
          point4:
            "Les joueurs ne peuvent pas prendre des pierres de plus d'une rangée en un seul tour.",
        },
        endgame: {
          title: "Fin de la partie",
          point1: "Le joueur qui prend la dernière pierre gagne.",
        },
      },

      othello: {
        game_title: "Règles de Othello",
        description:
          "Othello se joue à deux joueurs sur un plateau de 8×8 avec des disques ronds qui sont noirs d'un côté et blancs de l'autre. Chaque joueur dispose de plusieurs disques.",

        setup: {
          title: "Mise en place",
          point1: "Le jeu se joue sur un plateau de 8×8.",
          point2:
            "Chaque joueur reçoit un certain nombre de disques avec un côté noir et un côté blanc.",
          point3:
            "Au début du jeu, quatre disques sont placés dans une position prédéterminée au centre du plateau.",
        },

        gameplay: {
          title: "Déroulement du jeu",
          point1: "Le joueur noir commence toujours.",
          point2:
            "Un joueur doit placer un disque sur une case vide adjacente à un disque de l'adversaire, avec au moins un disque de l'adversaire entre le disque placé et un autre disque de la couleur du joueur.",
          point3:
            "Après avoir placé un disque, tous les disques de l'adversaire en ligne droite entre le nouveau disque et un autre disque de la couleur du joueur sont retournés.",
          point4:
            "Les joueurs jouent à tour de rôle. Si un joueur ne peut pas faire de mouvement retournant un disque de l'adversaire, il doit passer son tour.",
        },

        endgame: {
          title: "Fin de partie",
          point1:
            "Le jeu se termine lorsque le plateau est plein ou qu'aucun joueur ne peut faire de mouvement valide.",
          point2:
            "Le joueur ayant le plus de disques de sa couleur sur le plateau à la fin gagne.",
        },
      },

      checkers: {
        game_title: "Règles de dame",
        description:
          "Le jeu de dames est un jeu de société stratégique pour deux joueurs. Chaque joueur commence avec 12 pions, qui sont placés sur les cases sombres des trois rangées les plus proches de lui. Le but du jeu est de capturer ou de bloquer tous les pions de l'adversaire afin qu'ils ne puissent plus se déplacer.",

        setup: {
          title: "Le plateau de jeu au début",
          description:
            "Le plateau de dames est automatiquement placé de manière à ce qu'il y ait une case sombre en bas à gauche. Le premier joueur commence avec les pions blancs.",
        },

        movement: {
          title: "Le tirage des pierres",
          description:
            "Les pions se déplacent d'une case dans le sens de la diagonale, mais uniquement vers l'avant et uniquement sur des cases sombres libres.",
        },

        capturing: {
          title: "Frapper",
          description1:
            "Il y a une obligation de capture. Si vos propres pièces libres ne peuvent pas être cliquées pendant un coup, cela peut être dû au fait qu'il y a une possibilité de capture quelque part sur le plateau. Seule une de ces pièces peut alors être sélectionnée. Les simples pièces ne sont autorisées à capturer que vers l'avant. Lors de la capture, la pièce doit se trouver directement devant la pièce adverse et doit atterrir directement derrière la pièce capturée. Cette case doit être libre.",
          description2:
            "Si vous avez le choix entre différentes possibilités de capture, vous êtes libre de décider. Une exception est la capture multiple.",
          description3:
            "La capture multiple signifie: Si une pièce a capturé et qu'il est possible de capturer à nouveau avec la même pièce, le joueur continue son tour jusqu'à ce que les captures multiples ne soient plus possibles.",
        },

        queening: {
          title: "Convertir en dame",
          description1:
            "On obtient une dame lorsqu'un de ses pions s'arrête sur la ligne de base de l'adversaire, que ce soit par un coup normal ou par une prise. Le pion est alors marqué par une 'couronne' (dans le jeu de plateau, on place un deuxième pion dessus).",
          description2:
            "Une dame peut être déplacée en oblique vers l'avant ou vers l'arrière et il est également possible de frapper avec elle. Contrairement à la variante internationale de la dame, la dame ne peut se déplacer que d'une case en avant ou en arrière.",
        },

        endgame: {
          title: "Fin du jeu",
          description:
            "On a perdu quand on n'a plus de pion ou quand on ne peut plus faire de mouvement avec ses pions parce que ses pions sont bloqués par l'adversaire. On peut aussi perdre la partie par l'action 'abandonner', par exemple parce que l'on est tellement en retard que continuer à jouer n'a plus de sens.",
        },

        draw: {
          title: "Match nul",
          description:
            "Certaines parties se terminent par un match nul. Dans ce cas, aucun des deux joueurs ne peut plus gagner, à moins que l'autre ne fasse une énorme erreur. Pour éviter les parties interminables, il existe deux possibilités de match nul :",
          point1: "Les deux joueurs se sont mis d'accord sur ce point, ou",
          point2:
            "30 coups ont été tirés, au cours desquels aucun pion n'a été capturé.",
        },
      },
    },

//////////////////////////////////////////////////////////////////Anleitung//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    instructions: {
      instruction_title: "Documentation d'inscription",

      introduction: {
        title: "Introduction",
        description1: "Cette documentation décrit le processus d'utilisation d'une connexion WebSocket dans un langage de programmation sélectionné afin d'établir une connexion à l'URI wss://kimaster.mni.thm.de/ws. ",
        description2: "En outre, il décrit comment se connecter au réseau interne THM et envoyer des messages au format JSON et recevoir des retours du serveur.",
        description3:" Un exemple de connexion avec Python est également présenté.",
      },
      requirements: {
        title: "Conditions préalables",
        network_access:"Vous devez vous trouver dans le réseau interne du THM. Cela peut se faire soit via le VPN THM, soit via le réseau Eduroam.",
        websocket_uri: "WebSocket-URI: wss://kimaster.mni.thm.de/ws",
        browser_url: "Browser-URL: https://kimaster.mni.thm.de (pour les connexions via le navigateur)",
        message_format: "Format du message: JSON",
        documentation: "Documentation : Vous trouverez des informations sur les commandes JSON dans le fichier command.md.",
      },
      webSocketConnection: {
        title: "Verbindung mit Websocket",
        step1: {
          title: "Étape 1 : Créer un accès réseau",
          vpn: "THM VPN:",
          vpn_description: " Connectez-vous au VPN THM. Vous trouverez les instructions de configuration sur le site officiel de la THM.",
          vpn_link: "THM VPN Instructions",
          eduroam:"Réseau Eduroam: ",
          eduroam_description: "Alternativement, vous pouvez vous connecter au réseau Eduroam, si disponible.",
          eduroam_link: "Instructions Eduroam"
        },
        step2: {
          title: "Étape 2 : établir une connexion WebSocket",
          browser: {
            title: " Connexion par navigateur",
            open_browser: "1. ouvrez votre navigateur web",
            enter_url: "2. Saisissez l'URL https://kimaster.mni.thm.de.",
            internal_network: "3. Assurez-vous que vous vous trouvez dans le réseau interne THM.",
          },

          connection_with_ProgrammingLanguage: {
            title: "Lien avec un langage de programmation (exemple en Python)",
            install_python:"1. Installer Python : Assurez-vous que Python est installé sur votre ordinateur.",
            install_webSocket:"2. installer la bibliothèque WebSocket : Installez la bibliothèque WebSocket pour Python avec la commande suivante :",
            pip_command: "3. pip install websocket-client",
            connection_code: "Connection code:",
          },
        },
        step3: {
          title: "Étape 3 : Envoyer des messages JSON",
          json_format: "1. Formater un message JSON : ",
          json_format_descripton:"Tous les messages doivent être envoyés au format JSON.",
          example_message: "2. Exemple de message :",
          example_code: {
            command: "start_game",
            parameters: {},
          },

          send_message: "3. Envoyer un message :",
          send_message_description: "Utilisez la bibliothèque WebSocket du langage de programmation que vous avez choisi pour envoyer des messages.",
        },

        step4: {
          title: "Étape 4 : Recevoir une réponse",
          json_feedback: " 1.Confirmations JSON:",
          feedback: " Le serveur renvoie des réponses au format JSON.",
          bytestream: "2. Recevoir des bytestreams :",
          bytestream_receive: "Si le feed-back est un bytestream représentant un PNG, enregistrez-le en conséquence.",
        },
      },
    },
      footer: {
        datenschutz: 'Politique de Confidentialité',
        impressum: 'Mentions légales'
      },
  },
/////////////////////////////////////////////////////////Spanisch////////////////////////////////////////////////////////////////////////////////////////////////////
  
es: {
    message: {
      home: "Inicio",
      instruction: "Instrucción",
      leaderboard: "Tabla de clasificación",
      achievements: "Logros",
      welcome: "Bienvenido a KIMaster",
      subtitle: "Aquí puedes probar tu IA de juegos",
      enter_lobby_key: "Introducir la clave del vestíbulo",
      join_lobby: "Unirse al vestíbulo",
      lobby_join_failed: "¡Falló la unión al vestíbulo!",
      lobby_swap_failed: "Posición ocupada!",
      game_start_failed: "Cantidad incorrecta de jugadores!",
      joinAs: "Únete como",
      createLobby: "crear vestíbulo",
      create: "crear",
      chess: "Ajedrez",
      connect4: "Conecta 4",
      tictactoe: "Tres en raya",
      othello: "Othello",
      nim: "Nim",
      checkers: "Damas",
      leave_lobby: "Salir del vestíbulo",
      start_game: "¡Empezar el juego!",
      lobby_key_generating: "Clave del vestíbulo: Generando",
      lobby_key: "Clave del vestíbulo: {key}",
      your_position: "Tu posición {position}",
      lobby_position:
        "Posiciones de lobby: P1= {p1} P2= {p2} Espectadores {spectators}",
      lobbyPos: "Lobby Pos",
      lobbyStatus: "Estado del lobby",
      webSocketConnectionStatus: "Estado de la conexión WebSocket:",
      player1: "Jugador 1",
      player2: "Jugador 2",
      spectator: "Espectador",
      timeLine: "Línea del tiempo",
      player_vs_player: "Jugador contra Jugador",
      player_vs_ai: "Jugador contra KIM",
      playerai_vs_ai: "IA Jugador contra KIM",
      playerai_vs_playerai: "IA Jugador contra IA Jugador",
      KIM_vs_Player: "KIM contra los jugadores",
      KIM_vs_Player_AI: "KIM contra la IA",
      easy: "Fácil",
      medium: "Medio",
      hard: "Difícil",
      lobby: "Vestíbulo",
      lobby_welcome: "Bienvenido al vestíbulo de {game}",
      surrender: "Rendirse",
      quit_game: "Salir del juego",
      first: "Primero",
      previous: "Anterior",
      next: "Siguiente",
      last: "Último",
      undo_move: "Deshacer movimiento",
      new_game: "Nuevo juego",
      game_over: "Fin del juego",
      nim_move: "Hacer movimiento",
      row: "Fila",
      amount: "Cantidad",
      player_1_won: "El jugador 1 ganó",
      player_2_won: "El jugador 2 ganó",
      game_over_after: "Fin del juego después de",
      turn: "Turno",
      turns: "Turnos",
      okay: "Aceptar",
      show_rules: "regular",
      return_to_game: "Volver al juego",
      surrender_before_start:
        "Debes abandonar antes de poder empezar una nueva partida o lobby.",
      draw: "Indecisos!",
      startGame: "¡Que empiece el juego",
      waitMessage: "Esperar a que se cree el vestíbulo...",
      connection_not_possible: "La conexión con el servidor no ha sido posible",
      copyright: "© 2024 Tu empresa. Todos los derechos reservados.",
      step: "paso",
      unstep: "Deshacer el paso",
      evaluate: "evaluar",
      valid_Moves_Instead: "Valid Moves en lugar de Make Move",
      activateTwoTurnGame: "Activar dos rondas del juego",
      undo_this_num_of_terms: "Deshacer el número de revoluciones",
      grid_Width: "Ancho de rejilla",
      grid_Height: "Altura de la rejilla",
      play: "Jugar",
      received_from_server: "Recibido del servidor",
      command: "Comando",
      command_key: "Tecla de mando",
      key_value_pair_input: "Entrada de pares clave-valor",
      key: "Clave",
      value: "valor",
      add_pair: "Añadir par",
      json_output: "Salida JSON",
      your_turn: "Tu turno",
      opponent_turn: "Turno del adversario",
      blunder: "Muestra Errores",
      you_won: "¡Has ganado!",
      opponent_won: "El oponente ganó",
    },

    rules: {
      connect4: {
        game_title: "Reglas de las cuatro victorias",
        description:
          "Cuatro victorias es un juego para dos jugadores en el que, por turnos, dejan caer una ficha de su color en una de las siete columnas de la cuadrícula. El objetivo es ser el primero en tener cuatro fichas seguidas, ya sea en horizontal, vertical o diagonal.",

        setup: {
          title: "Preparación del juego",
          point1: "El tablero de juego consta de 7 columnas y 6 filas",
          point2:
            "Cada jugador elige un color y recibe un número ilimitado de fichas de ese color.",
        },

        gameplay: {
          title: "Jugabilidad",
          point1:
            "Por turnos, los jugadores dejan caer una piedra en una de las columnas.",
          point2:
            "La piedra cae en la posición más baja disponible de la columna.",
          point3:
            "El juego continúa hasta que un jugador tiene cuatro de sus piezas en fila o el tablero está lleno.",
        },
        endgame: {
          title: "Fin del juego",
          point1:
            "Un jugador gana cuando tiene cuatro fichas en fila (horizontal, vertical o diagonalmente).",
          point2:
            "El juego termina en tablas cuando el campo de juego está lleno y ningún jugador tiene cuatro fichas seguidas.",
        },
      },

      tictactoe: {
        game_title: "Reglas del tres en raya",
        description:
          "El tres en raya es un juego para dos jugadores en el que se turnan para marcar un cuadrado en una cuadrícula de 3x3. El objetivo es ser el primero en tener tres de tus personajes seguidos, ya sea en horizontal, vertical o diagonal.",

        setup: {
          title: "Preparación del juego",
          point1: "El campo de juego consiste en una cuadrícula de 3x3.",
          point2:
            "El juego continúa hasta que un jugador tiene tres de sus personajes seguidos o todos los espacios están ocupados.",
        },

        gameplay: {
          title: "Jugabilidad",
          point1:
            "Los jugadores se turnan para marcar una casilla en la cuadrícula.",
          point2:
            "El juego continúa hasta que un jugador tiene tres de sus personajes seguidos o todos los espacios están ocupados.",
        },

        endgame: {
          title: "Fin del juego",
          point1:
            "Un jugador gana si tiene tres personajes seguidos (horizontal, vertical o diagonalmente).",
          point2:
            "El juego termina en empate cuando todos los campos están ocupados y ningún jugador tiene tres personajes seguidos.",
        },
      },

      nim: {
        game_title: "Reglas de Nim",
        description:
          "Nim es un juego de estrategia donde los jugadores se turnan para quitar piedras de montones distintos. El jugador que quita la última piedra gana o pierde, dependiendo de la regla acordada.",

        setup: {
          title: "Preparación",
          point1: "Hay varias filas de piedras.",
          point2: "Dos jugadores se turnan.",
        },

        gameplay: {
          title: "Desarrollo del juego",
          point1:
            "Los jugadores se turnan para quitar piedras de una sola fila.",
          point2: "Un jugador debe tomar al menos una piedra en su turno.",
          point3: "Un jugador puede tomar varias piedras de la misma fila.",
          point4:
            "Los jugadores no pueden tomar piedras de más de una fila en un solo turno.",
        },

        endgame: {
          title: "Fin del juego",
          point1: "El jugador que toma la última piedra gana.",
        },
      },

      othello: {
        game_title: "Reglas de Othello",
        description:
          "Othello se juega entre dos jugadores en un tablero de 8×8 con discos redondos que son negros por un lado y blancos por el otro. Cada jugador recibe varios discos.",

        setup: {
          title: "Preparación",
          point1: "El juego se juega en un tablero de 8×8.",
          point2:
            "Cada jugador recibe un número de discos con un lado negro y un lado blanco.",
          point3:
            "Al comienzo del juego, cuatro discos se colocan en una posición predeterminada en el centro del tablero.",
        },

        gameplay: {
          title: "Desarrollo del juego",
          point1: "El jugador negro siempre mueve primero.",
          point2:
            "Un jugador debe colocar un disco en una casilla vacía adyacente a un disco del oponente, con al menos un disco del oponente entre el disco colocado y otro disco del color del jugador.",
          point3:
            "Después de colocar un disco, todos los discos del oponente en línea recta entre el nuevo disco y otro disco del color del jugador son volteados.",
          point4:
            "Los jugadores alternan turnos. Si un jugador no puede hacer un movimiento que voltee un disco del oponente, debe pasar.",
        },

        endgame: {
          title: "Fin del juego",
          point1:
            "El juego termina cuando el tablero está lleno o ninguno de los jugadores puede hacer un movimiento válido.",
          point2:
            "El jugador con más discos de su color en el tablero al final gana.",
        },
      },

      checkers: {
        game_title: "Reglas de las damas",
        description:
          "Las damas son un juego de mesa estratégico para dos jugadores. Cada jugador empieza con 12 fichas, que se colocan en las casillas oscuras de las tres filas más cercanas a él. El objetivo del juego es capturar o bloquear todas las fichas del adversario para que no puedan moverse.",

        setup: {
          title: "El tablero de juego al principio",
          description:
            "El tablero se coloca automáticamente de modo que haya una casilla oscura en la parte inferior izquierda. El jugador inicial comienza con las fichas blancas.",
        },

        movement: {
          title: "Tirando de las piedras",
          description:
            "Las piedras se mueven una casilla en diagonal, pero sólo hacia delante y sólo a casillas oscuras libres.",
        },

        capturing: {
          title: "Vencer a",
          description1:
            "Existe obligación de capturar. Si no se pueden hacer clic en tus propias piezas libres durante un movimiento, puede ser porque hay una oportunidad de captura en algún lugar del tablero. Solo una de estas piezas puede ser seleccionada. Las piezas simples solo pueden capturar hacia adelante. Al capturar, la pieza debe estar directamente frente a la pieza del oponente y debe aterrizar directamente detrás de la pieza capturada. Esta casilla debe estar libre.",
          description2:
            "Si tienes la opción entre diferentes oportunidades de captura, puedes decidir libremente. La excepción es la captura múltiple.",
          description3:
            "Captura múltiple significa: Si una pieza ha capturado y existe la posibilidad de capturar nuevamente con la misma pieza, el jugador continúa su turno hasta que la captura múltiple ya no sea posible.",
        },

        queening: {
          title: "Convertir en reina",
          description1:
            "Obtienes una dama si una de tus fichas se detiene en la línea de fondo de tu adversario, ya sea mediante un movimiento normal o una captura. La ficha se marca entonces con una 'corona' (en el juego de mesa, se coloca una segunda ficha encima).",
          description2:
            "Ahora la dama puede moverse en diagonal hacia delante y hacia atrás, y también se puede capturar con ella. Sin embargo, a diferencia de la variante de dama internacional, la dama sólo puede avanzar o retroceder una casilla.",
        },

        endgame: {
          title: "Fin del juego",
          description:
            "Has perdido si no tienes más piezas o si ya no puedes hacer ningún movimiento con tus piezas porque las tuyas están bloqueadas por tu adversario. También puedes perder la partida si realizas la acción 'Renunciar', por ejemplo, porque vas tan retrasado que ya no tiene sentido seguir jugando.",
        },

        draw: {
          title: "Dibujar",
          description:
            "Algunas partidas acaban en tablas. En tal caso, ningún jugador puede volver a ganar a menos que el otro cometa un error garrafal. Para evitar partidas interminables, hay dos posibilidades de tablas:",
          point1: "Ambos jugadores se han puesto de acuerdo",
          point2:
            "se realizaron 30 jugadas en las que no se capturó ninguna pieza.",
        },
      },
    },

    instructions: {
      instruction_title: "Instrucciones",
      introduction: {
        title: "Introducción",
        description1: "Esta documentación describe el proceso de utilización de una conexión WebSocket en un lenguaje de programación seleccionado para conectarse a la URI wss://kimaster.mni.thm.de/ws.",
        description2: "Además, explica cómo conectarse a la red interna de THM y enviar mensajes en formato JSON y recibir respuesta del servidor.",
        description3: "También se proporciona un ejemplo de conexión utilizando Python.",
      },
      requirements: {
        title: "Requisitos",
        network_access: "Debe estar en la red interna de THM. Puede hacerlo a través de la VPN de THM o de la red Eduroam.",
        websocket_uri_title: "WebSocket URI:",
        websocket_uri:" wss://kimaster.mni.thm.de/ws",
        browser_url_title: "Browser URL:",
        browser_url: " https://kimaster.mni.thm.de (para conexiones de navegador)",
        message_format_title: "Formato del mensaje: ",
        message_format: "JSON",
        documentation_title: "Documentación:",
        documentation: " Encontrará información sobre los comandos JSON en el archivo command.md."
      },
      webSocketConnection: {
        title: "Conexión WebSocket",
        step1: {
          title: "Paso 1: Establecer el acceso a la red",
          vpn: "THM VPN:",
          vpn_description: " Conéctese a la VPN de THM. Puedes encontrar instrucciones sobre cómo configurarlo en el sitio web oficial de THM.",
          vpn_link: "Guía THM VPN",
          eduroam:"Red Eduroam: ",
          eduroam_description: "También puede conectarse a la red Eduroam, si está disponible.",
          eduroam_link: "Guía Eduroam"
        },
        step2: {
          title: "Paso 2: Establecer conexión WebSocket",
          browser: {
            title: "Conexión a través del navegador",
            open_browser: "1. Abre tu navegador web.",
            enter_url: "2. Introduzca la URL https://kimaster.mni.thm.de.",
            internal_network: "3.Asegúrese de que se encuentra en la red interna de THM.",
          },
          connection_with_ProgrammingLanguage: {
            title: "Enlace con un lenguaje de programación (ejemplo en Python)",
            install_python:"1. Instalar Python : Asegúrese de que Python está instalado en su ordenador.",
            install_webSocket:"2. Instalar la librería WebSocket : Instale la librería WebSocket para Python con el siguiente comando :",
            pip_command: "3. pip install websocket-client",
            connection_code: "Código de conexión:",
          },
        },
        step3: {
          title: "Paso 3: Envío de mensajes JSON",
          json_format: "1. Formatear un mensaje JSON : ",
          json_format_descripton:"Todos los mensajes deben enviarse en formato JSON.",
          example_message: "2. Ejemplo de mensaje :",
          example_code: {
            command: "start_game",
            parameters: {},
          },

          send_message: "3. Enviar un mensaje :",
          send_message_description: "Utiliza la biblioteca WebSocket del lenguaje de programación que elijas para enviar mensajes.",
        },

        step4: {
          title: "Paso 4: Recibir una respuesta",
          json_feedback: " 1.Confirmaciones JSON:",
          feedback: " El servidor devuelve las respuestas en formato JSON.",
          bytestream: "2. Recibir bytestreams :",
          bytestream_receive: "Si la respuesta es un flujo de bytes que representa un PNG, guárdelo en consecuencia.",
        },
      },
    },
    footer: {
      datenschutz: 'Política de Privacidad',
      impressum: 'Pie de imprenta'
    },
  },
};

const i18n = createI18n({
  locale: "de", // Standard-Sprache
  fallbackLocale: "en", // Ausweichsprache
  messages,
});

export default i18n;
