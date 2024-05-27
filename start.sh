#!/bin/bash

# Build the Docker images
docker-compose build

# Start the swtp-server and swtp-frontend services in detached mode
docker-compose up -d swtp-server swtp-frontend
