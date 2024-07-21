# Projekt Dokumentation

## Inhaltsverzeichnis

3. [Dateistruktur](#dateistruktur)
4. [Verwendung](#verwendung)
5. [API-Beschreibung](#api-beschreibung)
6. [Klassen und Methoden](#klassen-und-methoden)
    - [Connection Manager](#connection-manager)
    - [Docker API](#docker-api)
    - [Lobby](#lobby)
    - [Lobby Manager](#lobby-manager)
    - [Socket Server](#socket-server)
    - [FastAPI Server](#fastapi-server)

## Voraussetzungen

- Ein System, das die Anforderungen von Docker erfüllt:
  - **Für Docker Desktop (Windows)**
    - Prozessor (CPU): 64-Bit mit Second Level Address Translation (SLAT)
    - Arbeitsspeicher (RAM): 4 GB
    - Betriebssystem: Windows 10 Home, Professional oder Enterprise
    - Virtualisierung: Hardware-Virtualisierung muss im BIOS des Computers aktiviert sein
    - Hyper-V: ist für Windows Professional oder Enterprise optional
    - Windows Subsystem für Linux 2 (WSL 2): muss für Windows Home aktiv sein
- Festplattenspeicher: min. 20 GB
- Internetverbindung: zum Herunterladen von Paketen
- Eine CUDA (12) fähige GPU (optional für das effiziente Trainieren neuer KIM Modelle)
- Für das Trainieren wird Python 3.11.1-3.11.12 benötigt.
- Git (optional)

## Installationsanweisungen

### Server und Docker

1. **Docker installieren**
    - Besuche die [Docker Desktop Webseite](https://www.docker.com/products/docker-desktop) und lade Docker Desktop herunter.
    - Folge den Installationsanweisungen für dein Betriebssystem (Windows, macOS, Linux).
    - Nach der Installation starte Docker Desktop und stelle sicher, dass es läuft.

2. **Ordner erstellen**
    - Erstelle einen Ordner, in den du das Git-Repository klonen möchtest oder in den du die ZIP-Datei entpacken möchtest.

3. **Repository klonen oder ZIP-Datei herunterladen**
    - **Option 1: Repository klonen**
        - Öffne ein Terminal (Command Prompt, PowerShell oder ein Unix-Terminal) und klone das GitHub-Repository:
          ```sh
          git clone https://github.com/12ghostrider21/Plattform-fuer-Vergleich-von-Spiele-KIs.git
          ```
    - **Option 2: ZIP-Datei herunterladen**
        - Gehe zur GitHub-Seite des Repositories.
        - Klicke auf den grünen "Code" Button und wähle "Download ZIP".
        - Entpacke die heruntergeladene ZIP-Datei in den zuvor erstellten Ordner.

4. **In das Verzeichnis wechseln**
    - Navigiere in das Verzeichnis des geklonten oder entpackten Repositories:
      ```sh
      cd PFAD/ZU/VERZEICHNIS
      ```
    - Ersetze `PFAD/ZU/VERZEICHNIS` durch den tatsächlichen Pfad zum geklonten oder entpackten Verzeichnis.

5. **Docker-Container starten**
    - **Windows**
        1. Stelle sicher, dass Docker Desktop läuft.
        2. Öffne ein Command Prompt oder PowerShell im Verzeichnis des geklonten oder entpackten Repositories.
        3. Führe die `start.cmd` Datei aus:
           ```sh
           start.cmd
           ```
    - **Unix (Linux, macOS)**
        1. Öffne ein Terminal im Verzeichnis des geklonten oder entpackten Repositories.
        2. Mache die `start.sh` Datei ausführbar (falls noch nicht geschehen):
           ```sh
           chmod +x start.sh
           ```
        3. Führe die `start.sh` Datei aus:
           ```sh
           ./start.sh
           ```


# Hauptklassen / Module
# Server

### `start.py`

Die Datei `start.py` initialisiert die FastAPI-Anwendung und konfiguriert die WebSocket-Endpunkte. Es erstellt Instanzen der Sprachbehandler, des SocketServers und des FastAPIServers.

**Hauptfunktionen:**
- `create_app()`: Erstellt die FastAPI-Anwendung und konfiguriert die WebSocket-Endpunkte.
  - Erstellt eine Instanz der `FastAPI`-Anwendung.
  - Initialisiert den `LanguageHandler` mit dem Pfad zur Sprachdatei.
  - Initialisiert den `SocketServer` mit dem `LanguageHandler`.
  - Initialisiert den `FastAPIServer` mit dem Socket-Manager, dem `LanguageHandler` und dem Importer des `SocketServer`.
  - Definiert die WebSocket-Endpunkte `/ws` und `/game`.
- Hauptskript zur Ausführung der Anwendung.
  - Wenn das Skript direkt ausgeführt wird, wird der Uvicorn-Server mit den Umgebungsvariablen `SERVER_HOST`, `SERVER_PORT` und `WORKER` gestartet.

### `connection_manager.py`

Diese Datei definiert eine abstrakte Klasse `AbstractConnectionManager`, die WebSocket-Verbindungen verwaltet.

**Hauptfunktionen:**
- Verwaltung aktiver Verbindungen (`active_connections`).
- Senden von Binärdaten und JSON-Antworten an WebSocket-Clients.
- Broadcasting von Nachrichten an mehrere Clients.
- Abstrakte Methoden zur Verwaltung von Verbindungen (`connect`, `disconnect`).

### `docker_api.py`

Diese Datei bietet eine Schnittstelle zur Verwaltung von Docker-Containern, die für Spielclients verwendet werden.

**Hauptfunktionen:**
- Initialisierung des Docker-Clients (`self.engine`).
- Auflisten aktiver Docker-Container (`list_containers`).
  - Gibt ein Wörterbuch mit Informationen über jeden Container zurück (ID, Name, Status, Image).
- Starten eines neuen Spielclient-Containers (`start_game_client`).
  - Startet einen neuen Docker-Container mit den Umgebungsvariablen `NETWORK`, `LOBBY_KEY`, `HOST_OF_API` und `SERVER_PORT`.
- Stoppen eines laufenden Spielclient-Containers (`stop_game_client`).
  - Stoppt den Container, der durch den Token identifiziert wird.
- Entfernen eines gestoppten Spielclient-Containers (`remove_game_client`).
  - Entfernt den Container, der durch den Token identifiziert wird.

### `lobby.py`

Die Datei `lobby.py` definiert die `Lobby`-Klasse, die die Spieler und Zuschauer in einer Spiel-Lobby verwaltet.

**Hauptfunktionen:**
- Initialisierung der Lobby mit einem eindeutigen Schlüssel (`self.key`).
  - Enthält Attribute für Spieler 1 (`self.p1`), Spieler 2 (`self.p2`), Spielschwierigkeit (`self.difficulty`), Spielmodus (`self.mode`), Spiel-Client (`self.game_client`), Zuschauer (`self.spectator_list`) und Spielstatus (`self.game_running`).
- Überprüfung, ob die Lobby leer ist (`is_empty`).
- Abrufen von WebSocket-Verbindungen basierend auf der Position (`get`).
- Überprüfung, ob ein Client bereits in der Lobby ist (`in_lobby`).
- Hinzufügen eines Clients zur Lobby (`join`).
  - Je nach Position wird der Client als Spieler 1, Spieler 2 oder Zuschauer hinzugefügt.
- Entfernen eines Clients aus der Lobby (`leave`).
  - Entfernt den Client aus der entsprechenden Position.
- Rollenwechsel eines Clients (`swap_to_p1`, `swap_to_p2`, `swap_to_spectator`).
  - Ändert die Rolle des Clients in Spieler 1, Spieler 2 oder Zuschauer.
- Abfrage des aktuellen Lobby-Status (`status`).
  - Gibt ein Wörterbuch mit Informationen über die Lobby zurück (Spieler 1, Spieler 2, Anzahl der Zuschauer, Spielclient, Spielstatus, Schlüssel).

### `lobby_manager.py`

Diese Datei verwaltet mehrere Lobbys und deren Lebenszyklus, einschließlich der Erstellung und Entfernung von Lobbys.

**Hauptfunktionen:**
- Erzeugung eines einzigartigen Lobby-Schlüssels (`_generate_lobby_key`).
  - Generiert einen eindeutigen Schlüssel basierend auf dem aktuellen UTC-Zeitstempel und einem SHA256-Hash.
- Erstellung einer neuen Lobby (`create_lobby`).
  - Erstellt eine neue Lobby mit einem eindeutigen Schlüssel und startet den zugehörigen Spielclient-Container.
- Überprüfung, ob eine Lobby existiert (`lobby_exist`).
  - Überprüft, ob eine Lobby mit dem gegebenen Schlüssel existiert.
- Entfernung einer Lobby (`remove_lobby`).
  - Entfernt die Lobby mit dem gegebenen Schlüssel.
- Verwaltung von Client-Operationen in Lobbys (`get_lobby`, `leave_lobby`, `join_lobby`, `swap_to`, `status_of_lobby`, `get_pos_of_client`).
  - Führt Operationen wie das Abrufen einer Lobby, das Verlassen einer Lobby, das Beitreten zu einer Lobby, das Wechseln der Position eines Clients und das Abfragen des Lobby-Status durch.
- Verwaltung von Spielclient-Operationen (`connect_game_client`, `disconnect_game_client`).
  - Verbindet und trennt Spielclients von Lobbys.

### `socketServer.py`

Die Datei `socketServer.py` erweitert `AbstractConnectionManager` und verwaltet WebSocket-Verbindungen sowie Spielinteraktionen.

**Hauptfunktionen:**
- Verbindungs- und Trennungsmanagement für WebSocket-Clients (`connect`, `disconnect`).
- Verwaltung von Spielzügen und -aktionen (`websocket_endpoint`).
  - Empfang und Verarbeitung von Nachrichten von WebSocket-Clients.
  - Verwaltung von Spielaktionen wie Spielupdates, KI-Züge, Blunder-Überprüfung und Zeichnung von Spielbrettern.
- Kommunikation mit dem Spielclient über WebSockets (`submit_task`, `player_to_pos`, `surface_to_png`, `kim_Action`, `draw`, `blunder`).
  - Ausführung von Aufgaben in einem eigenen Thread zur Reduzierung der Antwortzeiten.

### `fastAPIServer.py`

Diese Datei erweitert ebenfalls `AbstractConnectionManager` und bietet die Hauptlogik für den FastAPI-Server, der WebSocket-Verbindungen und Lobby-Management verarbeitet.

**Hauptfunktionen:**
- Verbindungs- und Trennungsmanagement für WebSocket-Clients (`connect`, `disconnect`).
- Haupt-Endpunkt für WebSocket-Verbindungen (`websocket_endpoint`).
  - Empfang und Verarbeitung von JSON-Daten von WebSocket-Clients.
- Verarbeitung von Debug-, Lobby- und Spielkommandos (`handle_debug_command`, `handle_lobby`, `handle_play_command`, `handle_client`).
  - Handhabung von Kommandos wie das Erstellen von Lobbys, Beitreten zu Lobbys, Verlassen von Lobbys, Rollenwechsel und Spielaktionen.

### `requirements.txt`

Diese Datei enthält die Abhängigkeiten des Servers.

**Hauptabhängigkeiten:**
- `h5py~=3.8.0`
- `fastapi==0.111.0`
- `uvicorn==0.30.1`
- `docker~=7.0.0`
- `requests < 2.32.0`
- `pygame==2.5.2`
- `numpy==1.26.4`
- `tensorflow~=2.14.0`
- `torch~=2.2.2`
- `tqdm~=4.66.4`
- `pandas~=2.2.2`
- `torchvision~=0.17.0`

## Aufbau und Funktion

Das Projekt ist modular aufgebaut, wobei jede Datei spezifische Funktionen für die Verwaltung von WebSocket-Verbindungen, Lobbys und Docker-Containern bereitstellt. Der Server nutzt FastAPI zur Bereitstellung von WebSocket-Diensten, die es ermöglichen, Echtzeitkommunikation mit den Spielclients zu führen.

### Ablauf

1. **Initialisierung**: Die Anwendung wird über `start.py` gestartet, wodurch die FastAPI-Anwendung erstellt und die WebSocket-Endpunkte konfiguriert werden.
2. **Lobby-Management**: `lobby_manager.py` verwaltet die Erstellung und den Lebenszyklus von Lobbys.
3. **WebSocket-Verbindungen**: `socketServer.py` und `fastAPIServer.py` handhaben die WebSocket-Verbindungen, empfangen und senden Nachrichten an die Clients.
4. **Spielverwaltung**: Über die WebSocket-Verbindungen werden Spielaktionen gesteuert und verwaltet.

# GameClient

### `start.py`

Die Datei `start.py` ist verantwortlich für die Konfiguration und Ausführung des Spielclients. Hier ist eine Aufschlüsselung ihrer Komponenten:

1. **Abrufen der Serverkonfiguration aus Umgebungsvariablen**:
   - **Serverport**: Der Serverport wird aus der Umgebungsvariable `SERVER_PORT` abgerufen. Wenn diese Variable nicht gesetzt ist, wird standardmäßig `8010` verwendet.
   - **Serverhost**: Der Serverhost wird aus der Umgebungsvariable `SERVER_HOST` abgerufen. Wenn diese Variable nicht gesetzt ist, wird standardmäßig `localhost` verwendet.
   - **Lobby-Schlüssel**: Der Lobby-Schlüssel wird aus der Umgebungsvariable `LOBBY_KEY` abgerufen. Wenn diese Variable nicht gesetzt ist, wird standardmäßig ein leerer String verwendet.

Der Lobby-Schlüssel hat hier mehrere Funktionen. Eine ist die der zuweisung welcher GameClient an welche Lobby behandelt. Mit diesem Key indentifiziert sich der GameClient beim Server, damit er immer die zuordnung Spiel zu Lobby treffen kann.
Sonnstige Umgebungsvariablen werden in der `docker-compose.yml` definiert.

### `connection_manager.py`

#### Hauptklasse
- **`WebSocketConnectionManager(ABC)`**
  - Diese Klasse verwaltet die WebSocket-Verbindung und verschiedene Kommunikationsbefehle.

#### Konstruktor
- **`__init__(self, host: str, port: int, key: str)`**
  - Initialisiert die WebSocket-Verbindung mit Host, Port und Schlüssel.
  - Setzt die URI für die Verbindung.

#### Methoden
- **`async def connect(self)`**
  - Stellt die Verbindung zum WebSocket-Server her.
  - Handhabt Verbindungsfehler.

- **`async def receive_json(self)`**
  - Empfängt und dekodiert JSON-Nachrichten vom WebSocket-Server.

- **`async def send_response(self, code: RCODE, to: str | None, data: dict = None)`**
  - Sendet eine Antwortnachricht im JSON-Format an den Server.

- **`async def send_cmd(self, command: str, command_key: str, p_pos: str | None, data: dict = None)`**
  - Sendet einen Befehl im JSON-Format an den Server.

- **`async def send_board(self, board: np.array, cur_player: int, game_name: str, valid: bool, from_pos: int | None)`**
  - Sendet den aktuellen Spielstatus an den Server.

- **`async def broadcast_board(self, board: np.array, cur_player: int, game_name: str, valid: bool)`**
  - Sendet den aktuellen Spielstatus an alle verbundenen Clients.

- **`async def close(self)`**
  - Schließt die WebSocket-Verbindung.

- **`async def __send_json(self, obj: json)`**
  - Hilfsmethode zum Senden von JSON-Nachrichten über die WebSocket-Verbindung.

### Zusammenfassung
Die Datei `connection_manager.py` definiert eine Klasse `WebSocketConnectionManager`, die eine WebSocket-Verbindung verwaltet und verschiedene Methoden zur Kommunikation mit einem WebSocket-Server bietet. Sie ermöglicht das Senden und Empfangen von JSON-Nachrichten, das Senden von Spielzuständen und Befehlen sowie das Schließen der Verbindung.


### `game_client.py`

#### Hauptklasse
- **`GameClient(WebSocketConnectionManager)`**
  - Diese Klasse erweitert `WebSocketConnectionManager` und verwaltet den Spielclient.

#### Konstruktor
- **`__init__(self, host: str, port: int, key: str)`**
  - Initialisiert den Spielclient mit Host, Port und Schlüssel.
  - Initialisiert den `Importer` und `Pit`.

#### Methoden
- **`async def run(self)`**
  - Hauptschleife, die den Spielclient ausführt und eingehende Befehle über eine WebSocket-Verbindung verarbeitet.

- **`def start_arena(self, board: np.array = None, cur_player: int = 1, it: int = 0)`**
  - Startet die Spielarena mit optionalem Anfangszustand, aktuellem Spieler und Iteration.

- **`def stop_arena(self)`**
  - Stoppt die Spielarena.

- **`def is_arena_running(self) -> bool`**
  - Überprüft, ob die Arena gerade läuft.

- **`async def update(self)`**
  - Sendet einen Update-Befehl an den WebSocket-Server mit dem aktuellen Spielstatus.

- **`@staticmethod def parse_input(input_str: str)`**
  - Parst den Eingabestring und konvertiert ihn in das entsprechende Format (Integer oder Tuple).

### Zusammenfassung
Die Datei `game_client.py` definiert eine Klasse `GameClient`, die `WebSocketConnectionManager` erweitert und Methoden zur Verwaltung eines Spielclients hinzufügt. Sie ermöglicht das Empfangen und Verarbeiten von Spielbefehlen, das Starten und Stoppen der Spielarena sowie das Aktualisieren des Spielstatus. Zusätzliche Hilfsmethoden unterstützen das Parsen von Eingaben und das Verwalten von Spielkonfigurationen.


### `pit.py`

#### Hauptklasse
- **`Pit`**
  - Diese Klasse verwaltet die Spielinteraktionen und -zustände.

#### Konstruktor
- **`__init__(self, game_client)`**
  - Initialisiert die Klasse `Pit` mit dem Spielclient.
  - Erstellt eine Instanz der Arena und zwei Spieler.

#### Methoden
- **`def clear_arena(self)`**
  - Setzt die Arena-Historie und andere Zustände zurück.

- **`def start_battle(self, board: np.array, cur_player: int, it: int)`**
  - Startet den Kampf in der Arena mit dem angegebenen Brettzustand, aktuellen Spieler und Iteration.

- **`def stop_battle(self)`**
  - Stoppt den Kampf in der Arena.

- **`def set_move(self, move, pos) -> bool`**
  - Setzt den Zug für einen Spieler basierend auf ihrer Position.

- **`def get_cur_player(self) -> int`**
  - Gibt den aktuellen Spieler zurück.

- **`def init_arena(self, game_config: GameConfig)`**
  - Initialisiert die Arena mit der Spielkonfiguration.

- **`def get_last_hist_entry(self) -> tuple[list | None, int | None, int | None]`**
  - Ruft den letzten Eintrag aus der Arena-Historie ab.

- **`def undo(self, steps: int) -> tuple[np.array, int, int]`**
  - Führt eine Rückgängig-Operation aus und gibt den Zustand des Spielfelds, den letzten Spieler und die Iteration zurück.

- **`def timeline(self, p_pos: str, forward: bool = True, start_index: int | None = None)`**
  - Navigiert durch die Spielzeitleiste vorwärts oder rückwärts.

- **`def set_blunder(self, blunder: list)`**
  - Setzt die Blunder-Liste in der Arena.

- **`def get_blunder_payload(self) -> dict`**
  - Gibt die Blunder-Payload zurück.

- **`def get_blunder(self, p_pos: str) -> dict`**
  - Gibt die Blunder-Daten für den angegebenen Spieler zurück.

### Zusammenfassung
Die Datei `pit.py` definiert eine Klasse `Pit`, die die Interaktionen und Zustände eines Spiels verwaltet. Sie bietet Methoden zum Starten und Stoppen des Kampfes, Setzen von Zügen, Rückgängig machen von Zügen, Navigieren durch die Spielzeitleiste und Verwalten von Blunder-Daten.

### `player.py`

#### Hauptklasse
- **`Player`**
  - Diese Klasse repräsentiert einen Spieler im Spiel.

#### Konstruktor
- **`__init__(self)`**
  - Initialisiert ein Player-Objekt mit Standardattributen.
  - Attribute:
    - `move`: Repräsentiert den aktuellen Zug des Spielers. Initial auf `None` gesetzt.
    - `send`: Ein Flag, das anzeigt, ob ein Zug gesendet wurde. Initial auf `False` gesetzt.

#### Methoden
- **`def play(self)`**
  - Verarbeitet und gibt den aktuellen Zug des Spielers zurück.
  - Setzt das Attribut `move` zurück auf `None`.
  - Rückgabe:
    - Der gemachte Zug oder `None`, wenn kein Zug gemacht wurde.

- **`def playAI(self)`**
  - Simuliert einen AI-Spieler, der einen Zug macht.
  - Überprüft das `send`-Flag, um zu bestimmen, ob ein Zug gemacht werden soll.
  - Rückgabe:
    - `True`, wenn ein AI-Zug gemacht werden soll.
    - Der gemachte Zug oder `None`, wenn kein Zug gemacht wurde.

### Zusammenfassung
Die Datei `player.py` definiert eine Klasse `Player`, die die grundlegenden Attribute und Methoden eines Spielers im Spiel enthält. Sie ermöglicht es, den aktuellen Zug des Spielers zu verarbeiten und zurückzugeben, sowie einen AI-Spieler zu simulieren.


### `requirements.txt`

Diese Datei enthält die Abhängigkeiten des GameClients.

**Hauptabhängigkeiten:**
- `websockets==12.0`
- `numpy~=1.26.4`


# Tools

### `rcode.py`
In dieser Datei befindet sich das RCODE-Enum welches alle möglichen Response Codes beinhaltet.

### `utils.py`

- **Attribute**:
  - `val`: Speichert den aktuellsten Wert.
  - `avg`: Speichert den laufenden Durchschnitt der Werte.
  - `sum`: Speichert die kumulative Summe aller Werte.
  - `count`: Speichert die Anzahl der hinzugefügten Werte.

- **Methoden**:
  - `__init__()`: Initialisiert die Attribute.
  - `__repr__()`: Gibt eine String-Repräsentation des laufenden Durchschnitts in wissenschaftlicher Notation mit zwei Dezimalstellen zurück.
  - `update(val, n=1)`: Aktualisiert den Zähler mit einem neuen Wert `val` und einem optionalen Gewicht `n` (Standard ist 1). Diese Methode berechnet den laufenden Durchschnitt neu.

### `dotdict` Klasse
Diese Klasse ist eine Unterklasse von `dict`, die den Zugriff auf Dictionary-Attribute mittels Punktnotation ermöglicht, sodass man auf Dictionary-Schlüssel zugreifen kann, als wären es Attribute.

- **Methoden**:
  - `__getattr__(name)`: Überschreibt die Standardmethode für den Attributzugriff, um den Wert zurückzugeben, der dem Schlüssel `name` zugeordnet ist. Wirft eine `AttributeError`, wenn der Schlüssel nicht im Dictionary existiert.

Beide Klassen bieten nützliche Funktionalitäten für die Handhabung von Metriken und Datenstrukturen in Dictionary-Form auf eine bequemere Weise.

### `neural_net.py`

- **`__init__(self, game)`**:
  - Initialisiert die Klasse. Diese Methode nimmt ein Spielobjekt als Argument, macht aber nichts weiter in der Basisimplementierung.

- **`train(self, examples)`**:
  - Trainiert das neuronale Netzwerk mit Beispielen, die aus selbst gespielten Partien stammen.
  - **Input**:
    - `examples`: Eine Liste von Trainingsbeispielen. Jedes Beispiel hat die Form `(board, pi, v)`, wobei `pi` der MCTS-informierte Policy-Vektor für das gegebene Brett ist und `v` dessen Wert darstellt. Die Beispiele enthalten das Brett in seiner kanonischen Form.

- **`predict(self, board)`**:
  - Gibt Vorhersagen für das aktuelle Brett in seiner kanonischen Form zurück.
  - **Input**:
    - `board`: Das aktuelle Brett in seiner kanonischen Form.
  - **Returns**:
    - `pi`: Ein Policy-Vektor für das aktuelle Brett, ein Numpy-Array der Länge `game.getActionSize`.
    - `v`: Ein Float-Wert im Bereich [-1,1], der den Wert des aktuellen Brettes angibt.

- **`save_checkpoint(self, folder, filename)`**:
  - Speichert das aktuelle neuronale Netzwerk (mit seinen Parametern) in `folder/filename`.

- **`load_checkpoint(self, folder, filename)`**:
  - Lädt die Parameter des neuronalen Netzwerks aus `folder/filename`.


### `mcts.py`

### Konstanten
- `EPS`: Ein kleiner Wert (`1e-8`), um Divisionen durch Null zu verhindern.

### Logging
- `log`: Logger für das Modul.

### `MCTS` Klasse
Die `MCTS` Klasse wird zur Initialisierung und Durchführung der Monte Carlo Tree Search verwendet.

#### Methoden

- **`__init__(self, game, nnet, args)`**:
  - Initialisiert das MCTS-Objekt mit dem Spiel, dem neuronalen Netzwerk und Argumenten.
  - **Parameter**:
    - `game`: Das Spielobjekt, das die spiel-spezifische Logik enthält.
    - `nnet`: Das neuronale Netzwerk, das zur Vorhersage von Policy und Wert verwendet wird.
    - `args`: Argumente, die verschiedene MCTS-Parameter enthalten.

- **`get_action_prob(self, board, cur_player, temp=1)`**:
  - Berechnet die Aktionswahrscheinlichkeiten für den gegebenen Brettzustand mithilfe von MCTS.
  - **Parameter**:
    - `board`: Der aktuelle Zustand des Bretts in seiner kanonischen Form.
    - `temp`: Temperaturparameter für die Exploration. Niedrigere Werte machen die Policy deterministischer.
    - `cur_player`: Der aktuelle Spieler.
  - **Rückgabe**:
    - Eine Liste von Aktionswahrscheinlichkeiten.

- **`search(self, board, cur_player)`**:
  - Führt eine einzelne MCTS-Suche vom gegebenen Brettzustand aus.
  - **Parameter**:
    - `board`: Der aktuelle Zustand des Bretts in seiner kanonischen Form.
    - `cur_player`: Der aktuelle Spieler.
  - **Rückgabe**:
    - Der negative Wert des Brettzustands aus der Perspektive des aktuellen Spielers.

#### Wichtige Attribute

- `Qsa`: Q-Werte für Zustand-Aktions-Paare.
- `Nsa`: Besuchszähler für Zustand-Aktions-Paare.
- `Ns`: Besuchszähler für Zustände.
- `Ps`: Initiale Policy, die vom neuronalen Netzwerk zurückgegeben wird.
- `Vs`: Gültige Züge für Zustände.
- `act`: Aktionstracking.
- `act_counter`: Aktionenzähler.
- `sanctioned_acts`: Liste der sanktionierten Aktionen, um Endlosschleifen zu vermeiden.

### Hauptfunktionen
- **`get_action_prob`** führt mehrere MCTS-Simulationen durch und berechnet die Wahrscheinlichkeiten der Aktionen basierend auf den Besuchszählern.
- **`search`** durchsucht den Baum rekursiv, wählt Aktionen basierend auf Upper Confidence Bound (UCB), und aktualisiert die Werte und Besuchszähler.

Diese Klasse und ihre Methoden bieten eine robuste Implementierung der Monte Carlo Tree Search für Entscheidungsfindung und Spielstrategie.

### `igame.py`

#### Methoden

- **`getInitBoard()`**:
  - Gibt das initiale Spielbrett als numpy-Array zurück und setzt alle anderen Daten auf den Anfangszustand zurück.
  - **Rückgabe**:
    - `startBoard`: Eine Darstellung des initialen Spielbretts, geeignet als Eingabe für ein neuronales Netzwerk.

- **`getBoardSize()`**:
  - Gibt die Dimensionen des Spielbretts zurück.
  - **Rückgabe**:
    - `x`: Die eindimensionale Größe des Spielbretts.
    - `(x, y)`: Ein Tupel, das die Anzahl der Reihen und Spalten des Spielbretts darstellt.

- **`getActionSize()`**:
  - Gibt die Gesamtzahl der möglichen Aktionen im Spiel zurück.
  - **Rückgabe**:
    - `actionSize`: Die Anzahl aller möglichen Aktionen im Spiel.

- **`getNextState(board, player, action)`**:
  - Generiert den nächsten Spielzustand nach der Anwendung der angegebenen Aktion für den aktuellen Spieler.
  - **Parameter**:
    - `board`: Das aktuelle Spielbrett als numpy-Array.
    - `player`: Der aktuelle Spieler (1 für einen Spieler, -1 für den anderen Spieler).
    - `action`: Die vom aktuellen Spieler auf dem Brett durchgeführte Aktion.
  - **Rückgabe**:
    - `nextBoard`: Das Spielbrett nach der Anwendung der angegebenen Aktion.
    - `nextPlayer`: Der Spieler, der im nächsten Zug spielt (sollte `-player` sein).

- **`getValidMoves(board, player)`**:
  - Bestimmt die gültigen Züge für den aktuellen Spieler auf dem gegebenen Brett in binärer Form.
  - **Parameter**:
    - `board`: Das aktuelle Spielbrett als numpy-Array.
    - `player`: Der aktuelle Spieler.
  - **Rückgabe**:
    - `validMoves`: Ein binärer Vektor, der gültige Züge anzeigt (1 für gültige Züge, 0 für ungültige Züge).

- **`getGameEnded(board, player)`**:
  - Bestimmt den Ausgang des Spiels für den gegebenen Spieler auf dem aktuellen Brettzustand.
  - **Parameter**:
    - `board`: Das aktuelle Spielbrett als numpy-Array.
    - `player`: Der aktuelle Spieler.
  - **Rückgabe**:
    - `result`: Ein Integer, der das Spielergebnis für den angegebenen Spieler darstellt (0 bei nicht beendeten Spielen, 1 bei Sieg, -1 bei Niederlage, kleiner nicht-Null-Wert bei Unentschieden).

- **`getSymmetries(board, pi)`**:
  - Generiert symmetrische Formen des gegebenen Bretts und des zugehörigen Policy-Vektors.
  - **Parameter**:
    - `board`: Das aktuelle Spielbrett als numpy-Array.
    - `pi`: Der Policy-Vektor, der Aktionswahrscheinlichkeiten angibt.
  - **Rückgabe**:
    - `symmForms`: Eine Liste von Tupeln (board, pi), wobei jedes Tupel eine symmetrische Form des Bretts und des zugehörigen Policy-Vektors darstellt.

- **`translate(board, player, index)`**:
  - Konvertiert einen Index von AlphaZero AI in eine Aktion.
  - **Parameter**:
    - `index`: Der Index des Zuges.
    - `board`: Das aktuelle Spielbrett als numpy-Array.
    - `player`: Der aktuelle Spieler.
  - **Rückgabe**:
    - `action`: Die Aktion, die dem Index entspricht.

- **`rotateMove(move)`**:
  - Rotiert einen Zug um 180 Grad, um ihn an ein rotierendes Spielfeld anzupassen.
  - **Parameter**:
    - `move`: Der zu rotierende Zug (kann ein Integer oder ein Tupel sein).
  - **Rückgabe**:
    - Der um 180 Grad gedrehte Zug.

- **`stringRepresentation(board)`**:
  - Konvertiert das aktuelle Spielbrett in ein String-Format, das für das Hashing in MCTS verwendet wird.
  - **Parameter**:
    - `board`: Das aktuelle Spielbrett als numpy-Array.
  - **Rückgabe**:
    - `boardString`: Eine String-Darstellung des Bretts, geeignet für das Hashing in MCTS.

- **`drawTerminal(board, valid_moves, cur_player, *args)`**:
  - Zeigt eine terminale Darstellung des Spielbretts zu Debugging-Zwecken an.
  - **Parameter**:
    - `board`: Das Spielbrett als numpy-Array.
    - `valid_moves`: Ob gültige Züge angezeigt werden sollen oder nicht.
    - `cur_player`: Der aktuelle Spieler.
    - `args`: Zusätzliche Argumente, wie `from_pos`.

- **`draw(board, valid_moves, cur_player, *args)`**:
  - Zeichnet die Spielrepräsentation auf eine Pygame-Oberfläche.
  - **Parameter**:
    - `board`: Das Spielbrett als numpy-Array.
    - `valid_moves`: Ob gültige Züge angezeigt werden sollen oder nicht.
    - `cur_player`: Der aktuelle Spieler.
    - `args`: Zusätzliche Argumente, wie `from_pos`.

Diese abstrakte Klasse legt die grundlegenden Methoden fest, die von jedem Spiel implementiert werden müssen, das in dieses Framework integriert wird.

# Language_Handler

Der Language Handler liest die `language.csv` ein und weist für jeden Spieler die Anworten der RCODES in der jeweiligen eingestellten Sprache zurück.
Sollte der Speicherort der **csv** geändert werden, dann muss der Pfad dieser Datei im `language_handler.py` nachgetragen werden.

### Verfügbare Sprachen:
- **EN** English
  - The most widely spoken language in the world, primarily used in the United Kingdom, the United States, and many other countries.
- **DE** Deutsch
  - The official language of Germany, Austria, and parts of Switzerland, known for its rich literary and philosophical traditions.
- **FR** Français
  - The official language of France and many African countries, renowned for its influence on art, cuisine, and diplomacy.
- **ES** Español
  - The second most spoken language in the world, primarily used in Spain and Latin America, celebrated for its vibrant culture and history.

Ergänze die CSV-Datei, die die Übersetzungen enthält, um die neuen Übersetzungen für die hinzugefügte Sprache. Jede Zeile der CSV-Datei sollte für jede unterstützte Sprache eine entsprechende Übersetzung enthalten.
Und Trage den jeweiligen neuen Sprach Key in der `language_handler.py` nach.

# dynamic_imports

Diese Datei dient dazu nur die verfügbaren Spiele zu erkennen und zu laden. Alle fehlenden Dateien beim Starten des Servers zu melden und dann das jeweilge Spiel zu ignorieren.
Für jedes Spiel ist eine genaue definition der Dateistruktur vorgesehen.

- Games
  - Ordner mit der Spienamen Bezeichnung
    - Spielname**Game**.py
    - Spielname**Logic**.py
    - pytorch
      - best.pth.tar
      - NNet.py
      - SpielnameNNet.py
    - keras
      - best.h5
      - NNet.py
      - SpielnameNNet.py
      
Das ist die Gewünchte Ordnerstruktur. Es ist nur notwendig den keras oder pytorch unterordner zu haben. Falls doch beide vorhanden sind, dann wird beim starten die pytorch implementation bevorzugt.
Beim Laden wird nicht auf groß oder kleinschreibung geachtet. Jedoch auf die Korrekte Endungen Game.py, Logic.py, NNet.py, best.pth.tar, best.h5. Sollten mehrere Modell Dateien mit best. vorhanden sein, dann wird die letzte gefundene genutzt.

# Trainer

## Voraussetzungen

Um neue Modelle für die KI KIM zu trainieren, müssen folgende Voraussetzungen erfüllt sein:

1. **Python-Umgebung**: Installieren Sie Python in der Version 3.11.x.
2. **Abhängigkeiten**: Installieren Sie die Abhängigkeiten aus der Datei `requirements.txt`, die sich im Ordner `Trainer` befindet.

    ```bash
    pip install -r Trainer/requirements.txt
    ```

## Hardware-Anforderungen

Das Training der Modelle kann sehr viel Arbeitsspeicher benötigen. Falls eine CUDA (12.1) fähige Grafikkarte vorhanden ist, können die Modelle deutlich schneller trainiert werden. Für unser Projekt wurde folgende Hardware verwendet:
- **CPU**: 24 Core Intel mit 6GHz
- **RAM**: 96 GB (64GB real, 32GB ausgelagert per SSD)
- **GPU**: RTX 4080 (Overclocked)
- **SPEICHER**: 4x 1TB SSD Raid 0 Setup mit 14GB/s kombiniert.

Die Trainingskonfiguration war wie folgt:
- **Iterationen**: 100
- **EPS**: 100
- **ArenaCompare**: 40

Die Trainingsdauer variiert je nach Spiel zwischen 1 und 27 Stunden. (Bei unserem System)

## Nutzung des Trainers

1. **Starten des Trainers**:
    - Starten Sie die Datei `main.py` mit der installierten Python-Umgebung.

    ```bash
    python main.py
    ```

2. **Spieleauswahl**:
    - Nach dem Start werden alle verfügbaren Spiele geladen und im Terminal zur Auswahl gestellt (von 0 bis x).

3. **Konfiguration der Trainingsparameter**:
    - Geben Sie die Anzahl der Iterationen, den EPS-Wert und den ArenaCompare-Wert im Terminal ein.

4. **Trainingsstart**:
    - Wenn alle Eingaben korrekt sind, lädt das System automatisch den letzten Trainingszustand und arbeitet die Konfiguration ab.
    - Sollte das Training unterbrochen werden und neu gestartet werden, beginnt es beim letzten Zwischenstand.

5. **Abschluss des Trainings**:
    - Wenn genügend trainiert wurde und ein Modell angenommen wird, wird der Ordner `checkpoints` mit den passenden Unterordnern erstellt.
    - In diesem Ordner finden Sie dann eine `best.h5` oder `best.path.tar`, welche die fertigen Modelle sind.

## Wichtige Hinweise

- **Trainingsdauer**: Je länger das Training dauert, desto stärker wird die KI. Allerdings wird jede Iteration zunehmend länger.
- **Abbruch und Neustart**: Das System speichert den Fortschritt, sodass beim Abbruch und Neustart des Trainings nicht von vorne begonnen werden muss.
