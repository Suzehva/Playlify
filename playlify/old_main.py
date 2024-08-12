from datetime import datetime
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
import requests

app = Flask(__name__)
app.secret_key = '???'

# these three should match with what is on Spotify developer dashboard
CLIENT_ID = '41434ef91b1144f5a58b9543e6cd6a77'
CLIENT_SECRET = '190e40fc8d1d4701b4ba9c3f968b78c8'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize' # to get token from spotify
TOKEN_URL = 'https://accounts.spotify.com/api/token' # to refresh token
API_BASE_URL = 'https://accounts.spotify.com/v1/'


@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login>Login with Spotify</a>" 

@app.route('/login')
def login():
    scope = 'playlist-modify-private playlist-modify-public' # might need user-read-email

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True, # only for testing purposes; remove for production (makes the user log in every time)
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


# this is what spotify comes back to after redirect from login
@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']}) # TODO: (suze) deal with errors better

    if 'code' in request.args:
        # information necessary to get access token
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI, # not used but necessary
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    
        response = requests.post(TOKEN_URL, data=req_body) # TODO: (suze) set timeout argument
        token_info = response.json()
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        # using timestamp because that removes the difficulty of dealing with timezones

        return redirect('/playlify')

#@app.route('/playlify')
