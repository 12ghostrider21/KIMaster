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
      nim:'Nim',
      checkers: 'Checkers',
      lobby_welcome: "Welcome to the",
      leave_lobby: "Leave Lobby",
      start_game: "Start Game",
      lobby_key_generating: "Lobby Key: Being Generated",
      lobby_key: "Lobby Key: {key}",
      your_position: "Your Position {position}",
      player1: "Player 1",
      player2: "Player 2",
      spectator: "Spectator",
      change_game_lobby: "Change to different Game Lobby:",
      player_vs_player: "Player vs Player",
      player_vs_ai: "Player vs KIM",
      playerai_vs_ai: "Player AI vs KIM",
      playerai_vs_playerai: "Player AI vs Player AI",
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
      copyright: "© 2024 Your Company. All rights reserved.",
    },

    rules: {
      connect4: {
        game_title: "Connect4 Rules",
        description: "Connect 4 is a two-player game where players take turns dropping their colored disc into a column. The objective is to be the first to get four of your discs in a row, either horizontally, vertically, or diagonally.",

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
          point2:
            "Each player chooses a mark, either 'X' or 'O'.",
        },
        gameplay: {
          title: "Gameplay",
          point1: "Players take turns marking a space in the grid.",
          point2:
            "The game continues until a player gets three of their marks in a row or all spaces are filled.",
        },
        endgame: {
          title: "Endgame",
          point1: "A player wins by getting three marks in a row (horizontally, vertically, or diagonally).",
          point2: "The game ends in a draw if all spaces are filled and no player has three marks in a row.",
        },
      },
      nim: {
        game_title: 'Nim Rules',
        description: "Nim is a strategy game where players take turns removing stones from distinct heaps. The player who removes the last stone wins.",

        setup: {
          title: "Setup",
          point1: "There are several rows of stones",
          point2: "Two player take turns"
        },

        gameplay: {
          title: "Gameplay",
          pont1: "Players take turns removing stones from a single row.",
          point2: "A player must take at least one stone on their turn.",
          point3: "A player may take multiple stones from the same row.",
          point4: "Players cannot take stones from more than one row in a single turn."
        },

        endgame: {
          title: "Endgame",
          point1: "The player who takes the last stone wins."
        }

      }
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
      nim: 'Nim',
      checkers: 'Dame',
      lobby_welcome: "Willkommen zur {game}",
      leave_lobby: "Lobby verlassen",
      start_game: "Spiel starten!",
      lobby_key_generating: "Lobby-Schlüssel: Wird generiert",
      lobby_key: "Lobby-Schlüssel: {key}",
      your_position: "Ihre Position {position}",
      player1: "Spieler 1",
      player2: "Spieler 2",
      spectator: "Zuschauer",
      change_game_lobby: "Zu anderem Spiel-Lobby wechseln:",
      player_vs_player: "Spieler gegen Spieler",
      player_vs_ai: "Spieler gegen KIM",
      playerai_vs_ai: "Spieler-KI gegen KIM",
      playerai_vs_playerai: "Spieler-KI gegen Spieler-KI",
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
          point2: "Jeder Spieler wählt eine Farbe und erhält eine unbegrenzte Anzahl an Steinen in dieser Farbe.",
        },
        gameplay: {
          title: "Spielablauf",
          point1: "Die Spieler lassen abwechselnd einen Stein in eine der Spalten fallen.",
          point2: "Der Stein fällt in die tiefste verfügbare Position in der Spalte.",
          point3: "Das Spiel geht weiter, bis ein Spieler vier seiner Steine in einer Reihe hat oder das Spielfeld voll ist.",
        },
        endgame: {
          title: "Spielende",
          point1: "Ein Spieler gewinnt, wenn er vier Steine in einer Reihe hat (horizontal, vertikal oder diagonal).",
          point2: "Das Spiel endet unentschieden, wenn das Spielfeld voll ist und kein Spieler vier Steine in einer Reihe hat.",
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
          point1: "Ein Spieler gewinnt, wenn er drei Zeichen in einer Reihe hat (horizontal, vertikal oder diagonal).",
          point2: "Das Spiel endet unentschieden, wenn alle Felder belegt sind und kein Spieler drei Zeichen in einer Reihe hat.",
        },
      },

      nim: {
        title: "Nim Regeln",
        description: "Nim ist ein Strategiespiel, bei dem die Spieler abwechselnd Steine aus verschiedenen Reihen nehmen. Der Spieler, der den letzten Stein nimmt, gewinnt.",
        setup: {
          title: "Spielvorbereitung",
          point1: "Es gibt mehrere Reihen von Steinen.",
          point2: "Zwei Spieler sind an der Reihe.",
        },

        gameplay: {
          title: "Spielablauf",
          point1: "Die Spieler nehmen abwechselnd Steine aus einer einzigen Reihe.",
          point2: "Ein Spieler muss mindestens einen Stein in seinem Zug nehmen.",
          point3: "Ein Spieler kann mehrere Steine aus derselben Reihe nehmen.",
          point4: "Die Spieler können nicht Steine aus mehr als einer Reihe in einem Zug nehmen.",
        },

        endgame: {
          title: "Spielende",
          point1: "Der Spieler, der den letzten Stein nimmt, gewinnt (oder verliert, je nach vereinbarter Regel).",
        },
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
      nim: 'Nim',
      checkers: 'Dame',
      leave_lobby: "Quitter la salle",
      start_game: "Commencer le jeu!",
      lobby_key_generating: "Clé de salle: Génération en cours",
      lobby_key: "Clé de salle: {key}",
      your_position: "Votre position {position}",
      player1: "Joueur 1",
      player2: "Joueur 2",
      spectator: "Spectateur",
      change_game_lobby: "Changer de salle de jeu:",
      player_vs_player: "Joueur contre Joueur",
      player_vs_ai: "Joueur contre KIM",
      playerai_vs_ai: "IA Joueur contre KIM",
      playerai_vs_playerai: "IA Joueur contre IA Joueur",
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
      copyright: "© 2024 Votre entreprise. Tous droits réservés.",
    },
    rules: {
      connect4: {
        game_title: 'Règles du jeu "Quatre gagnants',
        description: " Quatre gagnants est un jeu pour deux personnes dans lequel les joueurs font tomber à tour de rôle un pion de leur couleur dans l'une des sept colonnes de la grille. Le but est d'être le premier à aligner quatre pions, que ce soit horizontalement, verticalement ou en diagonale.",


        setup: {
          title: 'Préparation du jeu',
          point1: 'Le plateau de jeu se compose de 7 colonnes et 6 rangées',
          point2: 'Chaque joueur choisit une couleur et reçoit un nombre illimité de pions de cette couleur.',
        },

        gameplay: {
          title: 'Déroulement du jeu', 
          point1: 'Les joueurs marquent à tour de rôle une case de la grille.',
          point2: "La pierre tombe dans la position la plus basse disponible dans la colonne.",
          point3: "Le jeu se poursuit jusqu'à ce qu'un joueur ait aligné quatre de ses pions ou que le plateau de jeu soit plein."

        },
        endgame: {
          title: 'Fin du jeu',
          point1: "Un joueur gagne s'il a trois signes dans une rangée (horizontale, verticale ou diagonale).",
          point2: "Le jeu se termine par un match nul lorsque toutes les cases sont occupées et qu'aucun joueur n'a trois signes dans une rangée."
        }

      },

      tictactoe: {
        game_title: 'Règles du Tic Tac Toe',
        description: "Tic Tac Toe est un jeu à deux personnes dans lequel les joueurs marquent à tour de rôle une case dans une grille 3x3. Le but est d'être le premier à aligner trois de ses signes, que ce soit horizontalement, verticalement ou en diagonale.",

        setup: {
          title: 'Préparation du jeu',
          point1: "Le terrain de jeu se compose d'une grille de 3x3.",
          point2: "Chaque joueur choisit un signe, soit 'X', soit 'O'.",
        },

        gameplay: {
          title: 'Déroulement du jeu', 
          point1: '"Les joueurs marquent à tour de rôle une case de la grille.',
          point2: "Le jeu se poursuit jusqu'à ce qu'un joueur ait aligné trois de ses signes ou que toutes les cases soient occupées."

        },
        endgame: {
          title: 'Fin du jeu',
          point1: "Un joueur gagne s'il a trois signes dans une rangée (horizontale, verticale ou diagonale).",
          point2: "Le jeu se termine par un match nul lorsque toutes les cases sont occupées et qu'aucun joueur n'a trois signes dans une rangée."
        },
        
      },

      nim: {
        title: "Règles de Nim",
        description: "Nim est un jeu de stratégie où les joueurs prennent tour à tour des pierres dans des tas distincts. Le joueur qui enlève la dernière pierre gagne ou perd, selon la règle convenue.",
        setup: {
          title: "Préparation",
          point1: "Il y a plusieurs rangées de pierres.",
          point2: "Deux joueurs jouent à tour de rôle.",
        },
        gameplay: {
          title: "Déroulement du jeu",
          point1: "Les joueurs prennent à tour de rôle des pierres d'une seule rangée.",
          point2: "Un joueur doit prendre au moins une pierre à son tour.",
          point3: "Un joueur peut prendre plusieurs pierres de la même rangée.",
          point4: "Les joueurs ne peuvent pas prendre des pierres de plus d'une rangée en un seul tour.",
        },
        endgame: {
          title: "Fin de la partie",
          point1: "Le joueur qui prend la dernière pierre gagne (ou perd, selon la règle convenue).",
        },
      },

    }
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
      nim: 'Nim',
      checkers: 'Damas',
      leave_lobby: "Salir del vestíbulo",
      start_game: "¡Empezar el juego!",
      lobby_key_generating: "Clave del vestíbulo: Generando",
      lobby_key: "Clave del vestíbulo: {key}",
      your_position: "Tu posición {position}",
      player1: "Jugador 1",
      player2: "Jugador 2",
      spectator: "Espectador",
      change_game_lobby: "Cambiar a otro vestíbulo de juego:",
      player_vs_player: "Jugador contra Jugador",
      player_vs_ai: "Jugador contra KIM",
      playerai_vs_ai: "IA Jugador contra KIM",
      playerai_vs_playerai: "IA Jugador contra IA Jugador",
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
      copyright: "© 2024 Tu empresa. Todos los derechos reservados.",
    },

    rules: {
      connect4: {
        game_title: 'Reglas de las cuatro victorias',
        description: 'Cuatro victorias es un juego para dos jugadores en el que, por turnos, dejan caer una ficha de su color en una de las siete columnas de la cuadrícula. El objetivo es ser el primero en tener cuatro fichas seguidas, ya sea en horizontal, vertical o diagonal.',

        setup: {
          title: 'Preparación del juego',
          point1: 'El tablero de juego consta de 7 columnas y 6 filas',
          point2: 'Cada jugador elige un color y recibe un número ilimitado de fichas de ese color.',
        },

        gameplay: {
          title: 'Jugabilidad', 
          point1: 'Por turnos, los jugadores dejan caer una piedra en una de las columnas.',
          point2: 'La piedra cae en la posición más baja disponible de la columna.',
          point3: 'El juego continúa hasta que un jugador tiene cuatro de sus piezas en fila o el tablero está lleno.'

        },
        endgame: {
          title: 'Fin del juego',
          point1: 'Un jugador gana cuando tiene cuatro fichas en fila (horizontal, vertical o diagonalmente).',
          point2: 'El juego termina en tablas cuando el campo de juego está lleno y ningún jugador tiene cuatro fichas seguidas.'
        }

      },

      tictactoe: {
        game_title: 'Reglas del tres en raya',
        description: 'El tres en raya es un juego para dos jugadores en el que se turnan para marcar un cuadrado en una cuadrícula de 3x3. El objetivo es ser el primero en tener tres de tus personajes seguidos, ya sea en horizontal, vertical o diagonal.',

        setup: {
          title: 'Preparación del juego',
          point1: 'El campo de juego consiste en una cuadrícula de 3x3.',
          point2: 'El juego continúa hasta que un jugador tiene tres de sus personajes seguidos o todos los espacios están ocupados.',
        },

        gameplay: {
          title: 'Jugabilidad', 
          point1: 'Los jugadores se turnan para marcar una casilla en la cuadrícula.',
          point2: 'El juego continúa hasta que un jugador tiene tres de sus personajes seguidos o todos los espacios están ocupados.'

        },
        endgame: {
          title: 'Fin del juego',
          point1: 'Un jugador gana si tiene tres personajes seguidos (horizontal, vertical o diagonalmente).',
          point2: 'El juego termina en empate cuando todos los campos están ocupados y ningún jugador tiene tres personajes seguidos.'
        }
      },

      nim: {
        title: "Reglas de Nim",
        description: "Nim es un juego de estrategia donde los jugadores se turnan para quitar piedras de montones distintos. El jugador que quita la última piedra gana o pierde, dependiendo de la regla acordada.",
        setup: {
          title: "Preparación",
          point1: "Hay varias filas de piedras.",
          point2: "Dos jugadores se turnan.",
        },
        gameplay: {
          title: "Desarrollo del juego",
          point1: "Los jugadores se turnan para quitar piedras de una sola fila.",
          point2: "Un jugador debe tomar al menos una piedra en su turno.",
          point3: "Un jugador puede tomar varias piedras de la misma fila.",
          point4: "Los jugadores no pueden tomar piedras de más de una fila en un solo turno.",
        },
        endgame: {
          title: "Fin del juego",
          point1: "El jugador que toma la última piedra gana (o pierde, dependiendo de la regla acordada).",
        },
      },
    }
  },
};

const i18n = createI18n({
  locale: "de", // Standard-Sprache
  fallbackLocale: "en", // Ausweichsprache
  messages,
});

export default i18n;
