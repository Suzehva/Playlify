from datetime import datetime
from flask import Flask, redirect, request, session
import requests
import base64
from spot_search import spot_search

app = Flask(__name__)
app.secret_key = '???'

# these three should match with what is on Spotify developer dashboard
# TODO: (suze) do not just store client id's etc here
CLIENT_ID = '41434ef91b1144f5a58b9543e6cd6a77'
CLIENT_SECRET = '190e40fc8d1d4701b4ba9c3f968b78c8'
REDIRECT_URI = 'http://localhost:5000/callback'

TOKEN_URL = 'https://accounts.spotify.com/api/token' # to refresh token


@app.route('/')
def get_authorized():
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

    # store all received data
    token_info = response.json()
    session['access_token'] = token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    return redirect('/home_page')

@app.route('/home_page')
def home():
    return '''
        <form action="/main" method="get">
            <div style="text-align: center;">
                <h2>Playlify: Create a message hidden in a playlist</h2>
                <p>Give us some context!</p>
                
                <input type="text" name="context" placeholder="I want to propose to my girlfriend" 
                    style="display: block; width: 300px; padding: 10px; margin: 10px auto; border: 2px solid black; border-radius: 10px;">
                
                <p>Mood</p>
                <input type="text" name="mood" placeholder="love" 
                    style="display: block; width: 100px; padding: 10px; margin: 10px auto; border: 2px solid black; border-radius: 10px;">
                
                <input type="submit" value="submit" 
                    style="display: block; width: 100px; padding: 10px; margin: 20px auto; background-color: #ccc; border: 2px solid black; border-radius: 10px;">
            </div>
        </form>

    '''

@app.route('/main')
def main():
    ret_string = ""
    context = request.args.get('context')
    ret_string += "context: " + context + "\n"
    mood = request.args.get('mood')

    if 'access_token' not in session or datetime.now().timestamp() > session['expires_at']:
        return redirect('/')
    
    # TODO: call playlist_miner, collect list of songs

    spot_api_results = spot_search(session, context)
    ret_string += "spot_api_results: " + str(spot_api_results) + "\n"


    return ret_string


    # TODO: make file with common songs

    # TODO: call chatgpt to make sentence


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)