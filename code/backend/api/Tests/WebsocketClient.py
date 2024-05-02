import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8000/ws"  # Replace with your WebSocket server URI

    async with websockets.connect(uri) as websocket:
        print("WebSocket connection established.")

        while True:
            message = input("Type a message to send (or 'exit' to quit): ")

            await websocket.send(message)
            print(f"> Sent: {message}")

            if message.lower() == "exit":
                break



            response = await websocket.recv()
            print(f"< Received: {response}")

        print("Closing WebSocket connection.")
        await websocket.close()

asyncio.get_event_loop().run_until_complete(connect_to_server())
