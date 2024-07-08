import { createI18n } from "vue-i18n";

const messages = {
  en: {
    message: {
      home: "Home",
      instruction: "Instruction",
      leaderboard: "Leaderboard",
      achievements: "Achievements",
      welcome: "Welcome to KI-Master",
      subtitle: "Here you can test your Game-AI",
      enter_lobby_key: "Enter Lobby Key",
      join_lobby: "Join Lobby",
      lobby_join_failed: "Lobby Join Failed!",
      chess: "Chess",
      connect4: "Connect 4",
      tictactoe: "Tic Tac Toe",
      othello: "Othello",
      nim: "Nim",
      checkers: "Checkers",
      lobby_welcome: "Welcome to the",
      leave_lobby: "Leave Lobby",
      start_game: "Start Game",
      lobby_key_generating: "Lobby Key: Being Generated",
      lobby_key: "Lobby Key: {key}",
      your_position: "Your Position {position}",
      lobby_position:"Lobby Positions: P1= {p1} P2= {p2} Spectator {spectators}",
      player1: "Player 1",
      player2: "Player 2",
      spectator: "Spectator",
      change_game_lobby: "Change to different Game Lobby:",
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
      player_1_won: "Player 1 Won",
      player_2_won: "Player 2 Won",
      game_over_after: "Game over after",
      turns: "Turns",
      okay: "Okay",
      show_rules: "Rules",
      return_to_game: "Return to Game",
      surrender_before_start: "You need to first surrender before you can start a new Game or Lobby",
      draw: "Draw!",
      startGame: "Start Game!",
      waitMessage: "Waiting until Lobby is created...",
      copyright: "© 2024 Your Company. All rights reserved.",
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
          pont1: "Players take turns removing stones from a single row.",
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
            "The checkerboard is automatically placed so that a dark square is on the bottom left. The player with the black pieces starts.",
        },

        movement: {
          title: "Moving the Pieces",
          description:
            "Pieces move one square diagonally forward to an empty dark square.",
        },

        capturing: {
          title: "Capturing",
          description1:
            "Capturing is mandatory. If your pieces cannot be selected, it may be because a capture is possible. Only one of these pieces can be selected. Single pieces can only capture forward.",
          description2:
            "If you have a choice between different capture options, you are free to choose. Neither multiple captures nor captures with a king have absolute priority.",
        },

        queening: {
          title: "Queening",
          description1:
            "You get a queen when one of your pieces reaches the opponent's back row, either by a normal move or by a capture. The piece is marked with a 'Crown' (in the board game, a second piece is placed on top).",
          description2:
            "A queen can move diagonally both forward and backward and can also capture in both directions. Unlike international checkers, the king can only move one square forward or backward. When capturing, the queen must stand directly in front of the opponent's piece and land directly behind the captured piece.",
        },

        endgame: {
          title: "End of the Game",
          description:
            "You lose if you have no pieces left or if your pieces are blocked and cannot move. You can also concede the game by choosing 'Surrender'.",
        },

        draw: {
          title: "Draw",
          description:
            "Some games end in a draw. This happens when neither player can win unless the other makes a significant mistake. To prevent endless games, there are three ways to declare a draw:",
          point1: "Both players agree to a draw, or",
          point2:
            "25 moves have been made without a capture or promotion to a quuen, or",
          point3: "The same position occurs for the third time.",
        },
      },
    },
  },

  de: {
    message: {
      home: "Startseite",
      instruction: "Anleitung",
      leaderboard: "Rangliste",
      achievements: "Erfolge",
      welcome: "Willkommen zu KI-Master",
      subtitle: "Hier kannst du deine Spiele-KI testen",
      enter_lobby_key: "Lobby-Schlüssel eingeben",
      join_lobby: "Lobby beitreten",
      lobby_join_failed: "Lobbybeitritt fehlgeschlagen!",
      chess: "Schach",
      connect4: "Vier Gewinnt",
      tictactoe: "Tic Tac Toe",
      othello: "Othello",
      nim: "Nim",
      checkers: "Dame",
      lobby_welcome: "Willkommen zur {game}",
      leave_lobby: "Lobby verlassen",
      start_game: "Spiel starten!",
      lobby_key_generating: "Lobby-Schlüssel: Wird generiert",
      lobby_key: "Lobby-Schlüssel: {key}",
      your_position: "Ihre Position {position}",
      lobby_position: "Lobby Positionen: P1= {p1} P2= {p2} Zuschauer {spectators}",
      player1: "Spieler 1",
      player2: "Spieler 2",
      spectator: "Zuschauer",
      change_game_lobby: "Zu anderem Spiel-Lobby wechseln:",
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
      first: "Erster",
      previous: "Vorherige",
      next: "Nächste",
      last: "Letzte",
      undo_move: "Zug rückgängig machen",
      new_game: "Neues Spiel",
      game_over: "Spiel vorbei",
      player_1_won: "Spieler 1 hat gewonnen",
      player_2_won: "Spieler 2 hat gewonnen",
      game_over_after: "Spiel vorbei nach",
      turns: "Zügen",
      okay: "Okay",
      show_rules: "Regeln",
      return_to_game: "Zurück zum Spiel",
      surrender_before_start: "Sie müssen erst aufgeben, bevor Sie ein neues Spiel oder eine neue Lobby beginnen können",
      draw: "Unentschieden!",
      startGame: "Spiel Starten!",
      waitMessage: "Warten, bis die Lobby erstellt ist...",
      copyright: "© 2024 Dein Unternehmen. Alle Rechte vorbehalten.",
    },

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
        title: "Nim Regeln",
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
          point1:
            "Der Spieler, der den letzten Stein nimmt, gewinnt (oder verliert, je nach vereinbarter Regel).",
        },
      },

      othello: {
        title: "Othello Regeln",
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
            "Das Damebrett wird automatisch so platziert, dass links unten ein dunkles Feld liegt. Der Startspieler beginnt mit den schwarzen Steinen.",
        },

        movement: {
          title: "Das Ziehen der Steine",
          description:
            "Die Steine ziehen ein Feld in diagonaler Richtung, aber nur vorwärts und nur auf freie dunkle Felder.",
        },

        capturing: {
          title: "Schlagen",
          description1:
            "Es gilt Schlagzwang. Wenn sich eigene freie Steine bei einem Zug nicht anklicken lassen, kann das daran liegen, dass irgendwo auf dem Brett die Möglichkeit zum Schlagen besteht. Nur einer dieser Steine kann dann ausgewählt werden. Einfache Steine dürfen nur vorwärts schlagen.",
          description2:
            "Wenn man die Auswahl zwischen verschiedenen Schlagmöglichkeiten hat, darf man frei entscheiden. Weder ein Mehrfachschlagen, noch ein Schlagen mit einer Dame hat absoluten Vorrang.",
        },

        queening: {
          title: "In Dame umwandeln",
          description1:
            "Man bekommt eine Dame, wenn einer der eigenen Steine auf der gegnerischen Grundlinie stehen bleibt, egal ob durch einen normalen Zug oder durch ein Schlagen. Der Stein wird dann durch eine 'Krone' gekennzeichnet (im Brettspiel wird ein zweiter Stein darauf gestellt).",
          description2:
            "Eine Dame kanns nun sowohl schräg vorwärts als auch rückwärts bewegt werden und genauso darfst man mit ihr auch schlagen. Im Gegensatz zur internationalen Damenvariante darf sich die Dame aber nur um ein Feld vorwärts oder rückwärts bewegen. Beim Schlagen muss die Dame direkt vor dem gegnerischen Stein stehen und muss nach dem Schlagen direkt hinter dem geschlagenen Stein landen.",
        },

        endgame: {
          title: "Spielende",
          description:
            "Man hat verloren, wenn keinen Stein mehr hat oder wenn man mit seinen Steinen keinen Zug mehr machen kann, weil die eigenen Steine durch den Gegner blockiert sind. Man kann auch die Partie verloren geben durch die Aktion 'Aufgeben', zum Beispiel weil man so weit zurück liegt, dass ein weiteres Spielen keinen Sinn mehr macht.",
        },

        draw: {
          title: "Unentschieden",
          description1:
            "Manche Partien gehen unentschieden aus. In so einem Fall kann keiner der beiden Spieler mehr gewinnen, es sei denn, der andere macht einen enormen Fehler. Um endlose Partien zu vermeiden, gibt es drei Möglichkeiten für ein Unentschieden:",
          point1: "Beide Spieler sind sich darin einig geworden, oder",
          point2:
            "25 Züge wurden gezogen, in denen weder ein Stein geschlagen noch zur Dame umgewandelt wurde, oder",
          point3: "Eine Stellung wiederholt sich zum dritten Mal.",
        },
      },
    },

    fr: {
      message: {
        home: "Accueil",
        instruction: "Instruction",
        leaderboard: "Classement",
        achievements: "Réalisations",
        welcome: "Bienvenue chez KI-Master",
        subtitle: "Ici, vous pouvez tester votre IA de jeu",
        enter_lobby_key: "Entrez la clé de la salle",
        join_lobby: "Rejoindre la salle",
        lobby_join_failed: "Échec de la connexion à la salle!",
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
        lobby_position: "Positions du lobby: P1= {p1} P2= {p2} Spectateurs {spectators}",
        player1: "Joueur 1",
        player2: "Joueur 2",
        spectator: "Spectateur",
        change_game_lobby: "Changer de salle de jeu:",
        player_vs_player: "Joueur contre Joueur",
        player_vs_ai: "Joueur contre KIM",
        playerai_vs_ai: "IA Joueur contre KIM",
        playerai_vs_playerai: "IA Joueur contre IA Joueur",
        KIM_vs_Player: "KIM contre les joueurs",
        KIM_vs_Player_AI: "KIM contre joueur IA",
        easy: "Facile",
        medium: "Moyen",
        hard: "Difficile",
        lobby_welcome: "Bienvenue dans la salle de {game}",
        lobby: "Salle",
        surrender: "Abandonner",
        quit_game: "Quitter le jeu",
        first: "Premier",
        previous: "Précédent",
        next: "Suivant",
        last: "Dernier",
        undo_move: "Annuler le coup",
        new_game: "Nouveau jeu",
        game_over: "Fin du jeu",
        player_1_won: "Le joueur 1 a gagné",
        player_2_won: "Le joueur 2 a gagné",
        game_over_after: "Fin du jeu après",
        turns: "Tours",
        okay: "D'accord",
        show_rules: "réglementer",
        return_to_game: "Retour au jeu",
        surrender_before_start: "Vous devez abandonner avant de pouvoir commencer une nouvelle partie ou un nouveau lobby.",
        draw: "Match nul!",
        startGame: "Démarrer le jeu !",
        waitMessage: "Attendre que le lobby soit créé...",
        copyright: "© 2024 Votre entreprise. Tous droits réservés.",
      },

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
            point1:
              "Les joueurs marquent à tour de rôle une case de la grille.",
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
            point1:
              '"Les joueurs marquent à tour de rôle une case de la grille.',
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
          title: "Règles de Nim",
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
            point3:
              "Un joueur peut prendre plusieurs pierres de la même rangée.",
            point4:
              "Les joueurs ne peuvent pas prendre des pierres de plus d'une rangée en un seul tour.",
          },
          endgame: {
            title: "Fin de la partie",
            point1:
              "Le joueur qui prend la dernière pierre gagne (ou perd, selon la règle convenue).",
          },
        },

        othello: {
          title: "Règles de Othello",
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
          description: "Le jeu de dames est un jeu de société stratégique pour deux joueurs. Chaque joueur commence avec 12 pions, qui sont placés sur les cases sombres des trois rangées les plus proches de lui. Le but du jeu est de capturer ou de bloquer tous les pions de l'adversaire afin qu'ils ne puissent plus se déplacer.",

          setup: {
            title: "Le plateau de jeu au début",
            description: "Le plateau de dames est automatiquement placé de manière à ce qu'il y ait une case sombre en bas à gauche. Le premier joueur commence avec les pions noirs.",
           
          },

          movement: {
            title: "Le tirage des pierres",
            description: "Les pions se déplacent d'une case dans le sens de la diagonale, mais uniquement vers l'avant et uniquement sur des cases sombres libres."
          },

          capturing: {
            title: "Frapper",
            description1:
              "Il y a obligation de frapper. Si ses propres pions libres ne peuvent pas être cliqués lors d'un coup, cela peut être dû au fait qu'il existe quelque part sur le plateau la possibilité de frapper. Seul un de ces pions peut alors être sélectionné. Les pions simples ne peuvent que frapper en avant.",
            description2:
              "Si l'on a le choix entre plusieurs possibilités de frappe, on peut décider librement. Ni une frappe multiple, ni une frappe avec une dame n'ont la priorité absolue.",
          },
  
          queening: {
            title: "Convertir en dame",
            description1:
              "On obtient une dame lorsqu'un de ses pions s'arrête sur la ligne de base de l'adversaire, que ce soit par un coup normal ou par une prise. Le pion est alors marqué par une 'couronne' (dans le jeu de plateau, on place un deuxième pion dessus).",
            description2:
              "Une dame peut être déplacée en oblique vers l'avant ou vers l'arrière et il est également possible de frapper avec elle. Contrairement à la variante internationale de la dame, la dame ne peut se déplacer que d'une case en avant ou en arrière. Lors de la prise, la dame doit se trouver directement devant le pion adverse et doit atterrir après la prise directement derrière le pion pris.",
          },
  
          endgame: {
            title: "Fin du jeu",
            description:
              "On a perdu quand on n'a plus de pion ou quand on ne peut plus faire de mouvement avec ses pions parce que ses pions sont bloqués par l'adversaire. On peut aussi perdre la partie par l'action 'abandonner', par exemple parce que l'on est tellement en retard que continuer à jouer n'a plus de sens.",
          },
  
          draw: {
            title: "Match nul",
            description1:
              "Certaines parties se terminent par un match nul. Dans ce cas, aucun des deux joueurs ne peut plus gagner, à moins que l'autre ne fasse une énorme erreur. Pour éviter les parties interminables, il existe trois possibilités de match nul :",
            point1: "Les deux joueurs se sont mis d'accord sur ce point, ou",
            point2: "25 coups ont été tirés, au cours desquels aucun pion n'a été capturé ni transformé en dame, ou",
            point3: "Une position se répète pour la troisième fois.",
          },
        }
      },
    },

    es: {
      message: {
        home: "Inicio",
        instruction: "Instrucción",
        leaderboard: "Tabla de clasificación",
        achievements: "Logros",
        welcome: "Bienvenido a KI-Master",
        subtitle: "Aquí puedes probar tu IA de juegos",
        enter_lobby_key: "Introducir la clave del vestíbulo",
        join_lobby: "Unirse al vestíbulo",
        lobby_join_failed: "¡Falló la unión al vestíbulo!",
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
        lobby_position: "Posiciones de lobby: P1= {p1} P2= {p2} Espectadores {spectators}",
        player1: "Jugador 1",
        player2: "Jugador 2",
        spectator: "Espectador",
        change_game_lobby: "Cambiar a otro vestíbulo de juego:",
        player_vs_player: "Jugador contra Jugador",
        player_vs_ai: "Jugador contra KIM",
        playerai_vs_ai: "IA Jugador contra KIM",
        playerai_vs_playerai: "IA Jugador contra IA Jugador",
        KIM_vs_Player: "KIM contra los jugadores",
        KIM_vs_Player_AI: "KIM contra la IA",
        easy: "Fácil",
        medium: "Medio",
        hard: "Difícil",
        lobby_welcome: "Bienvenido al vestíbulo de {game}",
        lobby: "Vestíbulo",
        surrender: "Rendirse",
        quit_game: "Salir del juego",
        first: "Primero",
        previous: "Anterior",
        next: "Siguiente",
        last: "Último",
        undo_move: "Deshacer movimiento",
        new_game: "Nuevo juego",
        game_over: "Fin del juego",
        player_1_won: "El jugador 1 ganó",
        player_2_won: "El jugador 2 ganó",
        game_over_after: "Fin del juego después de",
        turns: "Turnos",
        okay: "Aceptar",
        show_rules: "regular",
        return_to_game: "Volver al juego",
        surrender_before_start: "Debes abandonar antes de poder empezar una nueva partida o lobby.",
        draw: "Indecisos!",
        startGame: "¡Que empiece el juego!",
        waitMessage: "Esperar a que se cree el vestíbulo...",
        copyright: "© 2024 Tu empresa. Todos los derechos reservados.",
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
          title: "Reglas de Nim",
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
            point1:
              "El jugador que toma la última piedra gana (o pierde, dependiendo de la regla acordada).",
          },
        },

        othello: {
          title: "Reglas de Othello",
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
              "El tablero se coloca automáticamente de modo que haya una casilla oscura en la parte inferior izquierda. El jugador inicial comienza con las fichas negras.",
          },
  
          movement: {
            title: "Tirando de las piedras",
            description:
              "Las piedras se mueven una casilla en diagonal, pero sólo hacia delante y sólo a casillas oscuras libres.",
          },
  
          capturing: {
            title: "Vencer a",
            description1:
              "Es obligatorio capturar. Si sus propias piezas libres no pueden ser pulsadas durante un movimiento, esto puede deberse a que hay una oportunidad de capturar en algún lugar del tablero. Sólo una de estas piezas puede entonces ser seleccionada. Las fichas simples sólo pueden capturar hacia delante.",
            description2:
              "Si puede elegir entre diferentes opciones de golpe, puede decidir libremente. Ni un golpe múltiple ni un golpe con reina tienen prioridad absoluta.",
          },
  
          queening: {
            title: "Convertir en reina",
            description1:
              "Obtienes una dama si una de tus fichas se detiene en la línea de fondo de tu adversario, ya sea mediante un movimiento normal o una captura. La ficha se marca entonces con una 'corona' (en el juego de mesa, se coloca una segunda ficha encima).",
            description2:
              "Ahora la dama puede moverse en diagonal hacia delante y hacia atrás, y también se puede capturar con ella. Sin embargo, a diferencia de la variante de dama internacional, la dama sólo puede avanzar o retroceder una casilla. Al capturar, la dama debe estar directamente delante de la pieza del adversario y debe caer directamente detrás de la pieza capturada tras la captura.",
          },
  
          endgame: {
            title: "Fin del juego",
            description:
              "Has perdido si no tienes más piezas o si ya no puedes hacer ningún movimiento con tus piezas porque las tuyas están bloqueadas por tu adversario. También puedes perder la partida si realizas la acción 'Renunciar', por ejemplo, porque vas tan retrasado que ya no tiene sentido seguir jugando.",
          },
  
          draw: {
            title: "Dibujar",
            description1:
              "Algunas partidas acaban en tablas. En tal caso, ningún jugador puede volver a ganar a menos que el otro cometa un error garrafal. Para evitar partidas interminables, hay tres posibilidades de tablas:",
            point1: "Ambos jugadores se han puesto de acuerdo",
            point2: "se realizaron 25 jugadas en las que no se capturó ninguna pieza ni se convirtió en dama, o",
            point3: "Se repite una posición por tercera vez.",
          },
        },

       
      },
    },
  },
};

const i18n = createI18n({
  locale: "de", // Standard-Sprache
  fallbackLocale: "en", // Ausweichsprache
  messages,
});

export default i18n;
