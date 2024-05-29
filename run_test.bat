docker-compose --profile test down -v
docker-compose down -v
docker-compose --profile test build
docker-compose  --profile test up --abort-on-container-exit