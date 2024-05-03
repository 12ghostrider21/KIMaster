import json
import socket
import threading


class GameClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345):
        """Initialize the GameClient with host, port, and game name."""
        self.host: str = host
        self.port: int = port
        self.client_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to the server and start a thread for receiving messages."""
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server {self.host}:{self.port}")
            threading.Thread(target=self.receive).start()  # Start a thread for receiving messages
        except ConnectionRefusedError:
            print(f"Connection to {self.host}:{self.port} failed.")

    def send_message(self, message: str):
        """Send a message (text or JSON) to the server."""
        try:
            self.client_socket.sendall(message.encode())  # Send the message as bytes
        except ConnectionError:
            print("Connection to the server lost.")

    def send(self, data):
        data_bytes = json.dumps(data).encode()
        # Sende die Länge der Daten
        self.client_socket.sendall(f"{len(data_bytes)}:{type(data).__name__}".encode())
        # Sende die Daten
        self.client_socket.sendall(data_bytes)

    def receive(self):
        """Continuously receive messages from the server."""
        while True:
            try:
                # Empfange die Datenlänge
                data_length, data_type = self.client_socket.recv(8).decode().split(":")

                # Empfange die Daten
                received_data = b""
                while len(received_data) < int(data_length):
                    packet = self.client_socket.recv(1024)
                    if not packet:
                        break
                    received_data += packet

                print("Received:", received_data)
                self.send("Hallo")

            except ConnectionError:
                print("Connection to the server lost.")
                break

    def close(self):
        """Close the client socket."""
        self.client_socket.close()


if __name__ == "__main__":
    g = GameClient()
    g.connect()
