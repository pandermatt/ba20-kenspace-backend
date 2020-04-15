# 🐍 BA20 KenSpace Backend
KenSpace: Explorative und komplexe Suchen auf unstrukturierte Dokumente

## Important Links

- https://github.com/pandermatt/BA20-KenSpace-Frontend
- https://github.com/pandermatt/BA20-KenSpace-Backend
- https://github.com/pandermatt/BA20-KenSpace-Documentation
- https://github.com/theCoder95/BA20-KenSpace-Research

## Developing

### Setup

```bash
git clone git@github.com:pandermatt/ba20-kenspace-backend.git
cd ba20-kenspace-backend
pip install -r requirements.txt
```

### Run
```bash
python app.py
```

#### Configuration

```bash
cp application.example.yml application.yml
```

Fill in all your keys

## Docker

Use the `Makefile`:

* `make build` builds the docker container
* `make run` runs the Flask App

## Access Docker file 

```bash
docker exec -it docker_kenspace_backend bash
```

or

```bash
docker ps
docker exec -it <docker-container> bash
```

### Clean up docker
- List all containers (only IDs) `docker ps -aq`
- Stop all running containers `docker stop $(docker ps -aq)`

**WARNING:** this will delete all your docker images
- Remove all containers `docker rm $(docker ps -aq)`
- Remove all images `docker rmi $(docker images -q)`


# Contributors
![](https://avatars2.githubusercontent.com/u/20790833?s=20) Pascal Andermatt

![]() Stefan Brunner
