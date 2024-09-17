
import requests
import base64
import urllib.parse
from dotenv import load_dotenv
import os

class Spotify():
    def __init__(self) -> None:
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = "http://buntes145.wohnheim.uni-kl.de/spotify/callback"

    def get_acces_token(self):
        SCOPE = "user-read-currently-playing"
        auth_url = "https://accounts.spotify.com/authorize"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": SCOPE,
        }

        auth_request_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
        return auth_request_url

    def get_currently_playing(self, token:str) -> dict:
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            current_track = response.json()
            return current_track
        else:
            print(f"Error: {response.status_code}")