from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import requests
import base64
import os
from dotenv import load_dotenv
import urllib.parse

spotify = Blueprint('spotify', __name__)

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:5000/spotify/callback"  # Adjust as needed
ACCESS_TOKEN = None
REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')

def refresh_access_token():
    global ACCESS_TOKEN
    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_creds_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        ACCESS_TOKEN = token_info['access_token']
    else:
        print("Failed to refresh access token.")
        ACCESS_TOKEN = None

@spotify.route('/')
def index():
    return render_template('spotify.html')

@spotify.route('/authorize')
def authorize():
    scope = "user-read-currently-playing"
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
    }
    return redirect(f"{auth_url}?{urllib.parse.urlencode(params)}")

@spotify.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_url = "https://accounts.spotify.com/api/token"
        client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

        headers = {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }

        response = requests.post(token_url, headers=headers, data=data)

        if response.status_code == 200:
            token_info = response.json()
            global ACCESS_TOKEN
            global REFRESH_TOKEN
            ACCESS_TOKEN = token_info['access_token']
            REFRESH_TOKEN = token_info['refresh_token']

            # Update .env file or save tokens securely here
            # Example: updating .env (not recommended for production)
            with open('.env', 'a') as f:
                f.write(f'SPOTIFY_REFRESH_TOKEN={REFRESH_TOKEN}\n')

            return redirect(url_for('spotify.currently_playing'))
        else:
            return jsonify({"error": "Failed to get tokens"}), response.status_code
    else:
        return jsonify({"error": "No code provided"}), 400

@spotify.route('/currently-playing')
def currently_playing():
    if ACCESS_TOKEN is None:
        refresh_access_token()

    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if not data:  # Check if the response is empty
            return jsonify({"message": "No track is currently playing"}), 204
        return jsonify(data)
    elif response.status_code == 401:  # Unauthorized
        # Try refreshing the token and retry
        refresh_access_token()
        headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:  # Check if the response is empty
                return jsonify({"message": "No track is currently playing"}), 204
            return jsonify(data)
        else:
            return jsonify({"error": "Unable to fetch currently playing track"}), response.status_code
    else:
        return jsonify({"error": "Unable to fetch currently playing track"}), response.status_code
