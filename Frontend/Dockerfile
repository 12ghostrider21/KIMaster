FROM node:lts-alpine    

WORKDIR /app

COPY ./Frontend/package.json .

RUN npm install -g http-server

WORKDIR /app/Frontend

ADD ./Frontend .

EXPOSE 8080

CMD [ "http-server", "dist" ]




