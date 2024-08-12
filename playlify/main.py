from datetime import datetime
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
import requests
import base64

app = Flask(__name__)
app.secret_key = '???'


# these three should match with what is on Spotify developer dashboard
CLIENT_ID = '41434ef91b1144f5a58b9543e6cd6a77'
CLIENT_SECRET = '190e40fc8d1d4701b4ba9c3f968b78c8'
REDIRECT_URI = 'http://localhost:5000/callback'

#AUTH_URL = 'https://accounts.spotify.com/authorize' # to get token from spotify
TOKEN_URL = 'https://accounts.spotify.com/api/token' # to refresh token
#API_BASE_URL = 'https://accounts.spotify.com/v1/'

@app.route('/')
def home():
    # get authorization with spotify set up
    token_data = {
        "grant_type": "client_credentials",
    }
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    
    response = requests.post(TOKEN_URL, data=token_data, headers=token_headers) # TODO: (suze) set timeout argument
    print("test2")
    print("token_headers: " + str(token_headers))
    print("token_data: " + str(token_data))

    # store all received data
    token_info = response.json()
    print("token_info: " + str(token_info))
    session['access_token'] = token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']



    # return welcome page
    return "Welcome to my Spotify App" 


if __name__ == "__main__":
    print("test1")
    app.run(host='0.0.0.0', debug=False)