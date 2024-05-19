FROM python:3.11.9

WORKDIR /app

ADD ./Server/requirements_server.txt .

RUN pip install -r requirements_server.txt

WORKDIR /app/Server

ADD ../Tools/e_response.py .

ADD ./Server .

CMD ["python", "-u", "StartServer.py"]