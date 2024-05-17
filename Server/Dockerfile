FROM python:3.11.9

WORKDIR /app

COPY ./Server/requirements_server.txt .

RUN pip install -r requirements_server.txt

COPY ./Server ./Server

ADD ../Tools/e_response.py ./Server

ENV PORT_TO_GAME_CLIENT=12345
ENV FAST_API_PORT=8000
ENV HOST_SOCKET_SERVER="0.0.0.0"
ENV HOST_FAST_API="0.0.0.0"

EXPOSE ${FAST_API_PORT}
EXPOSE ${PORT_TO_GAME_CLIENT}

WORKDIR /app/Server
 CMD ["python", "StartServer.py"]