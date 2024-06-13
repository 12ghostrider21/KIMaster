from docker import from_env
from os import environ, getenv
from docker.errors import ContainerError, ImageNotFound, APIError, NotFound, DockerException


class DockerAPI:
    image: str = "game-client-img"

    def __init__(self):
        try:
            self.engine = from_env()
        except DockerException:
            print(f"[DOCKER_API]: Engine not found! Maybe is Docker not started?")
            exit(1)
        self._debug: bool = False

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        self._debug = value

    def list_containers(self) -> dict:
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
        if self._debug:
            print(f"[DOCKER_API]: Starting GameClient: {token}")
        try:
            self.engine.containers.run(
                image=self.image,
                name=token,
                network=environ.get("NETWORK"),
                remove=self.debug,  # Remove container after it stops unless in debug mode
                detach=True,  # Run container in detached mode
                environment={
                    # Set environment variables for the container
                    'LOBBY_KEY': token,
                    'HOST_OF_API': getenv('HOST_OF_API', 'swtp-server'),
                    'SOCKET_SERVER_PORT': getenv('SOCKET_SERVER_PORT', '8000')
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
        if self._debug:
            print(f"[DOCKER_API]: Stopping GameClient: {token}")
        try:
            # Stop the container identified by the token
            self.engine.containers.get(token).stop()
            if self._debug:
                print(f'Successfully Stopped GameClient {token}')
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")

    def remove_game_client(self, token: str) -> None:
        if self._debug:
            print(f"[DOCKER_API]: Removing GameClient: {token}")
        try:
            # Remove the container identified by the token
            self.engine.containers.get(token).remove()
            if self._debug:
                print(f'[DOCKER_API]: Successfully GameClient {token} removed')
        except NotFound as e:
            # Handle case where the container is not found
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            # Handle general Docker API errors
            print(f"[DOCKER_API]: {e}")
