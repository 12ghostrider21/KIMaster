from GameClient import GameClient

if __name__ == "__main__":
    client = GameClient()

    try:
        client.connect()
        while True:
            message = input("Nachricht an Server (oder 'exit' zum Beenden): ")
            if message.lower() == "exit":
                break
            if message == "a":
                data = [1,2,3,4]
                client.send(data)
                continue

            if message == "d":
                data = {"key": "value", 1: 3.3}
                client.send(data)
                continue
            client.send(message)
    finally:
        client.close()