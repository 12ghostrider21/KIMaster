import json
import docker
import os
from docker.errors import ContainerError, ImageNotFound, APIError, NotFound

class DockerAPI:
    # Default Docker image for the game client
    image: str = "game-client-img"

    def __init__(self):
        # Initialize Docker client from environment
        self.engine = docker.from_env()
        # Debug flag for additional logging and keeping containers after they stop
        self.debug = False

    def toggle_debug(self) -> bool:
        """
        Toggles the debug mode.

        Returns:
            bool: The new state of the debug flag.
        """
        self.debug = not self.debug
        return self.debug

    def list_running_containers(self) -> dict:
        """
        Lists all currently running Docker containers.

        Returns:
            dict: A dictionary containing information about running containers.
        """
        container_info: dict = {}
        # Iterate over each running container
        for i, container in enumerate(self.engine.containers.list()):
            # Populate the dictionary with container details
            container_info["count"] = i + 1
            container_info[i] = {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags}
        return container_info

    def start_game_client(self, token: str) -> None:
        """
        Starts a new game client container.

        Args:
            token (str): The token to identify and name the container.
        """
        print(f'Trying to start GameClient: {token}')
        try:
            # Run a new container with the specified settings
            self.engine.containers.run(
                image=self.image,
                name=token,
                network=os.environ.get("NETWORK"),
                remove=not self.debug,  # Remove container after it stops unless in debug mode
                detach=True,  # Run container in detached mode
                environment={
                    # Set environment variables for the container
                    'LOBBY_KEY': token,
                    'HOST_OF_API': os.getenv('HOST_OF_API', 'swtp-server'),
                    'SOCKET_SERVER_PORT': os.getenv('SOCKET_SERVER_PORT', '12345')
                }
            )
            print(f'Successfully Started GameClient {token}')
        except ContainerError as e:
            # Handle container-specific errors
            print(f"[DOCKER_API]: {e}")
        except ImageNotFound as e:
            # Handle case where the specified image is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")

    def stop_game_client(self, token: str) -> None:
        """
        Stops a running game client container.

        Args:
            token (str): The token identifying the container to stop.
        """
        print(f'Trying to stop GameClient: {token}')
        try:
            # Stop the container identified by the token
            self.engine.containers.get(token).stop()
            print(f'Successfully Stopped GameClient {token}')
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")

    def remove_game_client(self, token: str) -> None:
        """
        Removes a stopped game client container.

        Args:
            token (str): The token identifying the container to remove.
        """
        print(f'Trying to remove GameClient: {token}')
        try:
            # Remove the container identified by the token
            self.engine.containers.get(token).remove()
            print(f'Successfully removed GameClient {token}')
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")
