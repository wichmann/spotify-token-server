
"""
A simple web server to regularly provide Spotify access tokens.

Source: https://developer.spotify.com/web-api/authorization-guide/#client-credentials-flow

Requiements:
- Flask
- APScheduler
- requests
"""

import json
import base64
import atexit
import logging

import requests
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

import config


app = Flask(__name__)

CURRENT_TOKEN = ''

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

logger = logging.getLogger('spotify_token_server')
logger.setLevel(logging.DEBUG)


@app.route("/")
def root():
    """Serve the current token as response."""
    return CURRENT_TOKEN


def update_token():
    """Update the global token from Spotify API."""
    global CURRENT_TOKEN
    CURRENT_TOKEN = get_token()


def get_token():
    """Get a new token from Spotify API."""
    url = 'https://accounts.spotify.com/api/token'
    client_id_and_secret = f"{config.SPOTIFY_CLIENT_ID}:{config.SPOTIFY_CLIENT_SECRET}"
    client_data = base64.urlsafe_b64encode(client_id_and_secret.encode()).decode()
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': f'Basic {client_data}'}
    payload = {'grant_type': 'client_credentials'}
    r = requests.post(url, headers=headers, data=payload, timeout=config.REQUESTS_TIMEOUT)
    server_data = json.loads(r.text)
    return server_data['access_token']


if __name__ == '__main__':
    logger.debug('Starting Spotify Token Server...')
    update_token()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_token, trigger="interval", minutes=config.TOKEN_UPDATE_INTERVAL)
    scheduler.start()
    # shut down the scheduler when exiting the app
    atexit.register(scheduler.shutdown)
    # start Flask HTTP server on port 5000
    app.run(host='0.0.0.0', port=5000)
