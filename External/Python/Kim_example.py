import asyncio
import json
import threading
from queue import Queue
from kim_interface import KIMaster


class Example(KIMaster):
    def __init__(self, uri_list: list[str]):
        """
        Initialize the Example class with a list of URIs.

        :param uri_list: List of URIs to connect to.
        """
        super().__init__(uri_list)
        # Queue for commands to be sent to the server
        self.command_queue: Queue = Queue()
        # Flag to control the input and handler loops
        self.exit: bool = False

    def input_thread(self) -> None:
        """
        Thread method to handle user input and enqueue commands.
        """
        while not self.exit:
            # Get command input from the user
            command = input("Command: ")
            if command == "exit":
                self.exit = True
                break
            # Get command key and data input from the user
            command_key = input("Command_key: ")
            data = input("Data: ")
            if data == "":
                data = None
            else:
                data = json.loads(data)
            # Enqueue the command, command_key, and data
            self.command_queue.put((command, command_key, data))

    async def send_handler(self) -> None:
        """
        Asynchronous handler to send commands from the queue to the server.
        """
        while not self.exit:
            if not self.command_queue.empty():
                # Get the next command from the queue and send it
                command, command_key, data = self.command_queue.get()
                await self.send_cmd(command, command_key, data)
            # Sleep briefly to allow other tasks to run
            await asyncio.sleep(0.1)
        # Close the connection when exiting
        await self.close()

    async def receive_handler(self) -> None:
        """
        Asynchronous handler to receive messages from the server.
        """
        while not self.exit:
            # Receive a message from the server
            message = await self.receive()
            if isinstance(message, dict):
                # Print the message if it is a dictionary
                self.print_message(message)
            if isinstance(message, bytes):
                # Show the image if the message is bytes
                self.show(message)
        # Close the connection when exiting
        await self.close()

    async def main(self) -> None:
        """
        Main method to establish connection and start handlers.
        """
        await self.connect()

        # Start the input thread to handle user input
        input_thread = threading.Thread(target=self.input_thread, daemon=True)
        input_thread.start()

        # Link both handlers to asyncio tasks and run them
        await self.handler(self.send_handler, self.receive_handler)


if __name__ == "__main__":
    # List of URIs to connect to
    uri = ["wss:/kimaster.mni.thm.de/ws", "ws://localhost:8010/ws"]
    # Create an instance of the Example class with the URI list
    master = Example(uri_list=uri)
    # Run the main method
    master.run(master.main())
