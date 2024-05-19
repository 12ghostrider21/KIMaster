FROM python:3.11.9

WORKDIR /app

ADD ./GameClient/requirements.txt .

RUN pip install -r requirements.txt

COPY ./GameClient ./GameClient

COPY  ../Tools ./GameClient

WORKDIR /app/GameClient

ENV PORT_TO_GAME_CLIENT=12345
ENV HOST_SOCKET_SERVER=swtp-server
ENV LOBBY_KEY=MISSING_LOBBY_KEY

EXPOSE ${PORT_TO_GAME_CLIENT}

CMD ["python", "-u", "StartClient.py"]



