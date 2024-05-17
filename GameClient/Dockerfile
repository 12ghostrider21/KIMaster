FROM python:3.11.9

WORKDIR /app

ADD ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ADD  ../Tools .

