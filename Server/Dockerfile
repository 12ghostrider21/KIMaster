FROM python:3.11.9

WORKDIR /app

COPY ./Server/requirements_server.txt .

RUN pip install -r requirements_server.txt

COPY ./Server ./Server

ADD ../Tools/e_response.py ./Server

WORKDIR /app/Server

CMD ["python", "-u", "StartServer.py"]