import asyncio
import json
import random

import websockets


async def listen_and_send(uri, key):
    async with websockets.connect(uri) as websocket:
        async def send_message(message):
            await websocket.send(message)
            print(f"Sent: {message}")

        async def receive_message():
            while True:
                message = None
                try:
                    message = await websocket.recv()
                    message = json.loads(message)
                except UnicodeDecodeError:
                    continue
                print(f"Received: {message}")
                if message.get("response_code") == 101:
                    await asyncio.sleep(1)
                    await send_message(json.dumps(
                        {"command": "play", "command_key": "create", "game": "connect4", "difficulty": "easy",
                         "mode": "player_vs_kim"}))
                    await asyncio.sleep(0.5)
                if message.get("response_code") == 218:
                    if message.get("cur_player") == 1:
                        await send_message(json.dumps({"command": "play", "command_key": "valid_moves"}))
                if message.get("response_code") == 208:
                    move = message.get("moves")
                    m = move[random.randint(0, len(move) - 1)]
                    await send_message(json.dumps({"command": "play", "command_key": "make_move", "move": m}))
                if message.get("response_code") == 202:
                    break

        receive_task = asyncio.create_task(receive_message())
        await asyncio.sleep(1)  # Eine kurze Wartezeit zum Initialisieren

        # Hier können Sie Nachrichten senden
        await send_message(json.dumps({"command": "lobby", "command_key": "join", "key": key}))

        await receive_task


async def main(key):
    uri = "ws://localhost:8010/ws"  # ws://localhost:8010/ws
    await listen_and_send(uri, key)


if __name__ == "__main__":
    key = "7a626"
    asyncio.run(main(key))
