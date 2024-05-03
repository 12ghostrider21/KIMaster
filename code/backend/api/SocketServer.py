import datetime
import socket
import threading
import json
from code.backend.api.Lobby import Lobby

class Server:

    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}  # Dictionary zur Verfolgung der verbundenen Clients
        self.lock = threading.Lock()
        self.lobbies: dict[str, Lobby] = {}

    def createLobby(self) -> dict:
        key = str(hash(datetime.datetime.now()))
        if key in self.clients.keys():
            raise KeyError(f"{key} already in use!")
        self.lobbies[key] = Lobby()
        return {"response": "create", "key": key}

    def start(self):
        """Startet den Server und wartet auf eingehende Verbindungen."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server läuft auf {self.host}:{self.port}...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection of {client_address}")

                # Neuen Thread starten, um die Verbindung mit dem Client zu behandeln
                client_thread = threading.Thread(target=self.client_connection,
                                                 args=(client_socket, client_address),
                                                 daemon=True)
                client_thread.start()
        except KeyboardInterrupt:
            print("Server wird heruntergefahren...")
        finally:
            self.server_socket.close()

    @staticmethod
    def send(sock, data):
        data_bytes = json.dumps(data).encode()
        # Sende die Länge der Daten
        sock.sendall(f"{len(data_bytes)}:{type(data).__name__}".encode())
        # Sende die Daten
        sock.sendall(data_bytes)

    def toServer(self, data) -> any:
        print(f"Server Recieved:", data)

    def client_connection(self, client_socket, client_address):
        """Behandelt die Verbindung mit einem Client in einem eigenen Thread."""

        with self.lock:
            if client_address[1] not in self.clients.keys():
                self.clients[client_address[1]] = client_socket
        try:
            while True:
                # Empfange die Datenlänge
                data_length, data_type = client_socket.recv(8).decode().split(":")

                # Empfange die Daten
                received_data = b""
                while len(received_data) < int(data_length):
                    packet = client_socket.recv(1024)
                    if not packet:
                        break
                    received_data += packet
                print(received_data, data_type)
                match data_type:
                    case "str":
                        string = str(received_data.decode())
                        print(string == "list", string, type(string))
                        match string:
                            case "list":
                                print("ABC")
                                Server.send(client_socket, [i for i in self.clients.keys()])

                    case "list":
                        pass
                    case "dict":
                        pass

        finally:
            # Verbindung schließen
            client_socket.close()
            print(f"Verbindung von {client_address} geschlossen")
            if client_address[1] in self.clients:
                del self.clients[client_address[1]]


if __name__ == "__main__":
    server = Server()
    server.start()
