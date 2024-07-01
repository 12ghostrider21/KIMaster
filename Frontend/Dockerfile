FROM node:lts-alpine    

WORKDIR /app

COPY ./Frontend/package.json ./

RUN npm install

WORKDIR /app/Frontend

COPY ./Frontend .

RUN npm run build

RUN npm install -g http-server

CMD [ "http-server", "dist" ]
