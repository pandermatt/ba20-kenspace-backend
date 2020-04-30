# 🪐🐍 BA20 KenSpace Backend
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

python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
```

For an easy installation, go to the Docker section.

### Run
```bash
python app.py
```

#### Configuration

```bash
cp application.example.yml application.yml
```

Fill in all your keys


## REST API

- `/upload/`: Upload your file to analyse
    - Method: `POST`
    - Params: `uploadType`: `csv`, `txt`, `whatsapp` or `zip`
    - Files: `file` with `FILE_CONTENT`
    - Headers: `Authorization: Bearer`
    - Returns: Data insight and `filename` of the Model. This `filename` must be included in the Cluster Settings.

- `/queries/`: Generate your Queries
    - Method: `GET`
    - Params: `uuid`: Model ID, `deletedWords`: Array of Deleted- / Stop words, `settings`
    - Headers: `Authorization: Bearer`
    - Returns: queries as JSON

- `/auth/`: Generate your Queries
    - Method: `GET`
    - Headers: `Authorization: Bearer`
    - Returns: `successful` if key is correct

- `/feedback/`: Submit feedback to your data
    - Method: `POST`
    - Params: 
        - `uuid`
        - `isHelpful`
        - `movieTitle`
        - `similarClusterActive`
        - `search`
        - `facet`
        - `delete`
        - `resultCount`
    - Headers: `Authorization: Bearer`
    - Returns: queries as JSON
    
- Settings Type
    - `display`: Title Column
    - `content`: Content Column
    - `filename`: Filename (response from upload)
    - `language`: Language to Analyse
    - `techniques`: `nltk` or `spacy`
    - `clusterSize`: `large`, `medium` or `small`
    - `itemToAnalyse`: `all` (display and content) or `content`
    
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
