FROM python:3.11.9-alpine

WORKDIR /app

ADD ./requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app/tests

ADD . .

CMD [ "pytest", "-v" , "-o log_cli=true"]