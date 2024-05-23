import docker
import os


class DockerAPI:

    def startGameClient(self, token: str):

        # init client to communicate with docker API 
        docker_client = docker.from_env()

        # perform docker run command, with config for a GameClient. 
        docker_client.containers.run('game-client-img',  # image to run
                                     name=token,  # set token as name of the container
                                     network=os.environ['NETWORK'],  # set network, to connect to on startup
                                     remove=False,
                                     # Set True to auto remove -
                                     # Can make debugging harder, because container logs will be removed too
                                     detach=True,  # Run container in detached mode
                                     environment={
                                         # Set Environment Variables (override defaults from GameClient Dockerfile)
                                         'LOBBY_KEY': token,
                                         'HOST_OF_API': os.getenv('HOST_OF_API', 'swtp-server'),
                                         'SOCKET_SERVER_PORT': os.getenv('SOCKET_SERVER_PORT', '12345')
                                     }
                                     )

    def stopGameClient(self, token: str):
        print(f'Trying to stop GameClient: {token}')
        docker_client = docker.from_env()

        try:
            docker_client.containers.get(token).stop()
            print(f'Successfully Stopped GameClient {token}')
        except docker.errors.NotFound:
            print(f'Failed Stopping GameClient {token} : docker could not find GameClient Container: {token}')
        except docker.errors.APIError:
            print(
                f'Failed Stopping GameClient {token}: '
                f'docker ran into an error, when trying to stop GameClient Container: {token}')

    def removeGameClient(self, token: str):
        print(f'Trying to remove GameClient: {token}')
        docker_client = docker.from_env()
        try:
            docker_client.containers.get(token).remove()
        except docker.errors.NotFound:
            print(f'Failed Removing GameClient {token} : docker could not find GameClient Container: {token}')
        except docker.errors.APIError:
            print(
                f'Failed Removing GameClient {token}: '
                f'docker ran into an error, when trying to remove GameClient Container: {token}')
