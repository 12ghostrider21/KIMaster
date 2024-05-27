@echo off
REM Stoppe und entferne alle Container, Netzwerke, Volumes und Images, die von docker-compose erstellt wurden
docker-compose down -v

REM Entferne alle ungenutzten Netzwerke
docker network prune -f --force

REM Entferne alle Docker-Images (optional)
docker-compose rm -f -v
for /F "delims=" %%i in ('docker images -q') do docker rmi %%i --force

REM Baue die Images neu ohne Cache, starte aber keine Container
docker-compose build --no-cache
