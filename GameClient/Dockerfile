FROM python:3.11.9-slim

# Specify default env here.
ENV LOBBY_KEY=MISSING_LOBBY_KEY
ENV SERVER_HOST=swtp-server
ENV SERVER_PORT=8000

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

WORKDIR /app
ADD ./GameClient/requirements.txt .
RUN pip install --no-deps --no-dependencies -r requirements.txt

# Set the working directory in the container
WORKDIR /app/GameClient

# Copy specific files from the Gameclient directory
ADD GameClient /app/GameClient

# Copy the Tools directory
ADD Tools /app/Tools

ADD Games /app/Games


# Run StartServer.py when the container launches
CMD ["python", "-u", "start.py"]