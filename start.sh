#!/bin/bash

docker-compose kill swtp-server swtp-frontend swtp-frontend-debug
docker-compose build
docker-compose up -d swtp-server swtp-frontend swtp-frontend-debug