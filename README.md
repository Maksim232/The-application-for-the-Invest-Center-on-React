# Installation
## Install docker
#### On Windows
##### Windows 11 or with winget installed
```pwsh
wsl --install -d Ubuntu
winget install Docker.DockerDesktop -h
```
##### Below Windows 11
[Installer](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
#### On Linux
```bash
# install docker
curl -sSL https://get.docker.com | sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker; exit

# install docker compose
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -i) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```
#### On MacOS
[Installer](https://docs.docker.com/desktop/install/mac-install/)
##### Apple Silicon launch instruction
Due to some issues with several python packages (like asyncpg), which haven't builds for linux aarch64, you should use buildx
```zsh
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up -d --build
# Then to accelerate frontend, if you are frontend dev, build frontend without buildx
docker-compose up -d --build frontend
```
## Launch app in development mode
###### Note, that on windows you must use WSL if you are frontend developer due to react-scripts@5.0.0 bug with hot reloading
```bash
docker compose up -d --build
```
## Launch app in production mode
```bash
docker compose -f "docker-compose.prod.yml" up -d --build
```
# Project TODO
- fill todo
