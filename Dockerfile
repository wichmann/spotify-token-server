# Dockerfile for spotify_token_server

# set base image for Python apps
FROM python:3.13-alpine

LABEL org.opencontainers.image.title="spotify_token_server"
LABEL org.opencontainers.image.description="A simple web server to regularly provide Spotify access tokens."
LABEL org.opencontainers.image.version="0.2"
LABEL org.opencontainers.image.authors="wichmann@bbs-os-brinkstr.de"
LABEL org.opencontainers.image.licenses="MIT License"
LABEL org.opencontainers.image.documentation="https://github.com/wichmann/spotify-token-server/blob/master/README.md"
LABEL org.opencontainers.image.source="https://github.com/wichmann/spotify-token-server"

ENV SPOTIFY_TOKEN_SERVER_RUNNING_AS_CONTAINER=1
WORKDIR /app

# setup Python libs
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy app to container
COPY app.py /app
COPY config.py /app

# expose port
EXPOSE 5000

# set command
ENTRYPOINT [ "python" ]
CMD ["app.py" ]
