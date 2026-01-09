[![MIT License](https://img.shields.io/badge/license-MIT-red.svg?style=flat)](http://choosealicense.com/licenses/mit/)

# spotify_token_server
A simple web server to regularly provide Spotify access tokens.

## Usage
To start the web app with the internal web server of Flask:

    FLASK_DEBUG=True pipenv run python app.py

## Docker
To build the image just execute the following command:

    docker image build -t spotify-token-server .

When running the container you can specify your actual configuration by
overwriting the existing file inside the container:

    docker run -p 5000:5000 -v ./config.actual.py:/app/config.py -d spotify-token-server

If you are using docker compose with a traefik reverse proxy, the configuration
could look like this:

    services:
      spotify-token-server:
        # build image manually from source
        # build: https://github.com/wichmann/spotify-token-server.git
        # image: spotify-token-server
        image: ghcr.io/wichmann/spotify-token-server:main
        restart: always
        ports:
          - 5000:5000
        volumes:
          - ./config.actual.py:/app/config.py
        labels:
        - "traefik.enable=true"
        - "traefik.http.services.spotify-token-server.loadbalancer.server.port=5000"
        - "traefik.http.routers.spotify_tokspotify-token-serveren_server.rule=Host(`token.domain.com`)"
        - "traefik.http.routers.spotify-token-server.tls=true"
        - "traefik.http.routers.spotify-token-server.tls.certresolver=letsencrypt"

## Requirements
Install all necessary dependencies with:

    pip install -r requirements.txt
