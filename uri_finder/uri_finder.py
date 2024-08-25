"""
Usage: 
    1. put a list of songs you want to process in input_songs.txt (only the name). 
    2. run python uri_finder.py (make sure you're in the directory with this file)
    3. get the songs and uri's from the output_songs.txt file and add them to common_words.txt
"""
from playlify.utils import search_spotify
from flask import Flask, redirect, request, session
from playlify.constants import CLIENT_ID, CLIENT_SECRET, TOKEN_URL
import base64
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = '???'

# TODO: integrate this with auth setup once we have that
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


def main():
    input_file_path = 'input_songs.txt'
    song_set = set()

    # make a list of songs
    with open(input_file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace (including newlines)
            song = line.strip()
            if song:
                response = search_spotify(session, query=song, offset=0, limit=1, search_type="track")
                track = response['tracks']['items'][0]
                # check that the returned song is the same on we requested
                if track['name'] != song: 
                    # find a few more songs, maybe song will be in here
                    responses = search_spotify(session, query=song, offset=1, limit=10, search_type="track")
                    tracks = responses['tracks']['items']
                    success = False
                    for track in tracks:
                        if track['name'] == song:
                            song_set.add((track['name'], track['uri']))
                            success = True
                            break
                    if not success:
                        raise ValueError(f"Song requested {song} could not be found in spotify database")
                else:
                    song_set.add((track['name'], track['uri']))

    # add songs to new file
    output_file_path = 'output_songs.txt'
    with open(output_file_path, 'w') as file:
        for song, uri in song_set:
            line = f"{song},{uri}\n"
            # Write the formatted string to the file
            file.write(line)

if __name__ == "__main__":
    main()