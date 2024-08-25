"""
uri_finder.py processed a txt file input_songs and adds the uri's of 
songs with those names to a file output_songs.

Usage: 
    1. put a list of songs you want to process in input_songs.txt (only the name). 
    2. run python uri_finder.py (make sure you're in the directory with this file)
    3. get the songs and uri's from the output_songs.txt file and add them to common_words.txt
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playlify.utils import search_spotify
from playlify.constants import CLIENT_ID, CLIENT_SECRET, TOKEN_URL
import base64
import requests
from datetime import datetime

# Simple dictionary to store token info
token_info = {}

def get_authorized():
    global token_info
    # get authorization with spotify set up
    token_data = {
        "grant_type": "client_credentials",
    }
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    response = requests.post(TOKEN_URL, data=token_data, headers=token_headers)

    # store all received data
    token_info = response.json()
    token_info['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

def main():
    get_authorized()  # Get the access token before searching

    input_file_path = 'input_songs.txt'
    song_set = set()
    failed_songs = set()

    # make a list of songs
    with open(input_file_path, 'r') as file:
        for line in file:
            song = line.strip()
            if song:
                response = search_spotify(token_info, query=song, offset=0, limit=1, search_type="track")
                track = response['tracks']['items'][0]
                if track['name'].lower() != song.lower(): 
                    print("looking for: " + song)
                    print("found: " + track['name'])
                    responses = search_spotify(token_info, query=song, offset=1, limit=20, search_type="track")
                    tracks = responses['tracks']['items']
                    success = False
                    for track in tracks:
                        print("found more: " + track['name'])
                        if track['name'].lower() == song.lower():
                            song_set.add((track['name'], track['uri']))
                            success = True
                            break
                    if not success:
                        failed_songs.add(song)
                else:
                    song_set.add((track['name'], track['uri']))

    # add songs to new file
    output_file_path = 'output_songs.txt'
    with open(output_file_path, 'w') as file:
        for song, uri in song_set:
            line = f"{song},{uri}\n"
            file.write(line)
    
    if len(failed_songs) > 0:

        raise ValueError("Some requested songs could not be found in spotify database: ", str(failed_songs))

if __name__ == "__main__":
    main()