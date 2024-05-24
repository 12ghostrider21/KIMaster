FROM python:3.11.9

# Specify default env here. 
ENV LOBBY_KEY=MISSING_LOBBY_KEY
ENV HOST_OF_API=swtp-server
ENV SOCKET_SERVER_PORT=12345
# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

WORKDIR /app
ADD ./GameClient/requirements.txt .
RUN pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /app/GameClient

# Copy specific files from the Gameclient directory
ADD GameClient /app/GameClient

# Copy the Tools directory
ADD Tools /app/Tools

# Run StartServer.py when the container launches
CMD ["python", "-u", "StartClient.py"]



