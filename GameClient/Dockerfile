FROM python:3.11.9

WORKDIR /app

ADD ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ADD  ../Tools .

ENV PORT_TO_GAME_CLIENT=12345
ENV HOST_SOCKET_SERVER="0.0.0.0"
ENV LOBBY_KEY="e318ad20ae5b57426f8970a2fe644942740d2c1e2554c327ff4449029b0109c1"

EXPOSE ${PORT_TO_GAME_CLIENT}

CMD ["python", "StartClient.py"]



