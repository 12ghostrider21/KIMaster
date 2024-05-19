FROM python:3.11.9

# Specify default env here. 
ENV LOBBY_KEY=MISSING_LOBBY_KEY
ENV HOST_OF_API=swtp-server
ENV SOCKET_SERVER_PORT=12345

WORKDIR /app

ADD ./GameClient/requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app/GameClient

ADD ./GameClient .

ADD  ../Tools .

CMD ["python", "-u", "StartClient.py"]



