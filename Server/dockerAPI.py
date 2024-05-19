import docker
import os
import time

class DockerAPI:

    def startGameClient(self, token:str):
        print(f"Starting Client: {token}")
        client = docker.from_env()
        print("\n\n\n#############################################################")
        
        #
        lobby = client.containers.create('game-client-img', 
                                         name=token, 
                                         network=os.environ["NETWORK"],
                                         environment= [f"LOBBY_KEY={token}"])
            
        print("#############################################################\n\n\n")


    def stopGameClient(self, token:str):
        pass

