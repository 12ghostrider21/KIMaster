import json

import docker
import os
from docker.errors import ContainerError, ImageNotFound, APIError, NotFound


class DockerAPI:
    image: str = "game-client-img"

    def __init__(self):
        self.engine = docker.from_env()
        self.debug = False

    def toggle_debug(self) -> bool:
        self.debug = not self.debug
        return self.debug

    def list_running_containers(self) -> dict:
        container_info: dict = {}
        for i, container in enumerate(self.engine.containers.list()):
            container_info["count"] = i
            container_info[i] = {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags}
        return container_info

    def start_game_client(self, token: str) -> None:
        print(f'Trying to start GameClient: {token}')
        try:
            self.engine.containers.run(
                image=self.image,
                name=token,
                network=os.environ.get("NETWORK"),
                remove=not self.debug,
                detach=True,
                environment={
                    # Set Environment Variables (override defaults from GameClient Dockerfile)
                    'LOBBY_KEY': token,
                    'HOST_OF_API': os.getenv('HOST_OF_API', 'swtp-server'),
                    'SOCKET_SERVER_PORT': os.getenv('SOCKET_SERVER_PORT', '12345')
                }
            )
            print(f'Successfully Started GameClient {token}')
        except ContainerError as e:
            print(f"[DOCKER_API]: {e}")
        except ImageNotFound as e:
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            print(f"[DOCKER_API]: {e}")

    def stop_game_client(self, token: str) -> None:
        print(f'Trying to stop GameClient: {token}')
        try:
            self.engine.containers.get(token).stop()
            print(f'Successfully Stopped GameClient {token}')
        except NotFound as e:
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            print(f"[DOCKER_API]: {e}")

    def remove_game_client(self, token: str) -> None:
        print(f'Trying to remove GameClient: {token}')
        try:
            self.engine.containers.get(token).remove()
            print(f'Successfully removed GameClient {token}')
        except NotFound as e:
            print(f"[DOCKER_API]: {e}")
        except APIError as e:
            print(f"[DOCKER_API]: {e}")
