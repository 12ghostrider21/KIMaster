FROM node:lts-alpine    

WORKDIR /app

COPY ./Frontend/package.json ./Frontend/package-lock.json ./

RUN npm install

WORKDIR /app/Frontend

COPY ./Frontend .

RUN npm run build

RUN npm install -g http-server

EXPOSE 8080

CMD [ "http-server", "dist" ]
