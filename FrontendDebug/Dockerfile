FROM node:lts-alpine    

WORKDIR /app

COPY ./FrontendDebug/package.json ./

RUN npm install

WORKDIR /app/FrontendDebug

COPY ./FrontendDebug .

RUN npm run build

RUN npm install -g http-server

CMD [ "http-server", "dist" ]
