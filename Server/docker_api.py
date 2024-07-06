import docker 
from os import environ, getenv
from docker.errors import ContainerError, ImageNotFound, APIError, NotFound


class DockerAPI:
    """
    Class to interact with Docker to manage game client containers.

    Attributes:
        image (str): The Docker image name for the game client.
        engine: The Docker client initialized from the environment.
        _debug (bool): Flag to enable or disable debug mode.
    """
    image: str = "game-client-img"  # name of docker image

    def __init__(self):
        """
        Initialize the DockerAPI class, setting up the Docker client.
        """
        self.engine = docker.from_env()
        self._debug: bool = True

    @property
    def debug(self) -> bool:
        """
        Get the debug mode status.

        Returns:
            bool: The current status of debug mode.
        """
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        """
        Set the debug mode status.

        Args:
            value (bool): The new status for debug mode.
        """
        self._debug = value

    def list_containers(self) -> dict:
        """
        List all active Docker containers.

        Returns:
            dict: A dictionary with information about each container.
        """
        container_info: dict = {}
        for i, container in enumerate(self.engine.containers.list()):
            container_info["count"] = i + 1
            container_info[i] = {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags}
        return container_info

    def start_game_client(self, token: str) -> None:
        """
        Start a new game client container.

        Args:
            token (str): The unique token for the game client.
        """
        if self._debug:
            print(f"[DOCKER_API]: Starting GameClient: {token}")
        try:
            self.engine.containers.run(
                image=self.image,
                name=token,
                network=environ.get("NETWORK"),
                remove=not self.debug,  # Remove container after it stops unless in debug mode
                detach=True,  # Run container in detached mode
                environment={
                    # Set environment variables for the container
                    'LOBBY_KEY': token,
                    'HOST_OF_API': getenv('HOST_OF_API', 'swtp-server'),
                    'SERVER_PORT': getenv('SERVER_PORT', '8010')
                }
            )
            if self._debug:
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
        Stop a running game client container.

        Args:
            token (str): The unique token for the game client.
        """
        try:
            # Stop the container identified by the token
            self.engine.containers.get(token).kill()
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")

    def remove_game_client(self, token: str) -> None:
        """
        Remove a stopped game client container.

        Args:
            token (str): The unique token for the game client.
        """
        try:
            # Remove the container identified by the token
            self.engine.containers.get(token).remove()
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")
