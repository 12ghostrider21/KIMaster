# Use the official Python image based on a slim version.
# Since every Lobby is running in one single instance of this Image, these Container need to be as small as possible.
# The slim version is crucial here since it provides an excelent compromise between size and range of mandatory functions
# The Python version is 3.11.9.
FROM python:3.11.9-slim

# Set default environment variables.
ENV LOBBY_KEY=MISSING_LOBBY_KEY

# Those are a fallbacks to the code inside the ./Server/docker_api.py to ensure those Environment Variables are initialized with a default value. 
# If the swtp-server isn't capable of providing the GameClients with those defaults should be used automatically.
# This level of redundancy makes it harder to change the Port and Host. 
# When changing the port Remember to change it everywhere in the entire Project to make sure it is consistent 
ENV SERVER_HOST=swtp-server
ENV SERVER_PORT=8010

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Set the working directory in the container to /app.
WORKDIR /app

# Copy the requirements.txt file from the local ./GameClient directory to the current working directory in the container.
ADD ./GameClient/requirements.txt .

# Install the Python dependencies specified in requirements.txt without installing dependencies of dependencies.
RUN pip install --no-deps --no-dependencies -r requirements.txt

# Change the working directory in the container to /app/GameClient.
WORKDIR /app/GameClient

# Copy the entire contents of the local GameClient directory to /app/GameClient in the container.
ADD GameClient /app/GameClient

# Copy the entire contents of the local Tools directory to /app/Tools in the container. This works because of the build context specified in the docker-compose.yml
ADD Tools /app/Tools

# Copy the entire contents of the local Games directory to /app/Games in the container. This works because of the build context specified in the docker-compose.yml
ADD Games /app/Games

# Run StartServer.py when the container launches
CMD ["python", "-u", "start.py"]