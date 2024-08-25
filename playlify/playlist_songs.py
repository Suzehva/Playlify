"""
playlist_songs.py contains the functions used to get songs 
from playlists gathered by the user's input mood
"""
import requests
from typing import Set
from utils import search_spotify
from playlify.constants import PLAYLIST_AMOUNT, PLAYLIST_OFFSET


def collect_playlist_songs(session, mood: str) -> Set:
    results = set()
    mood = mood.split()
    for word in mood:
        response_dict = search_spotify(session, query=word, offset=PLAYLIST_OFFSET, limit=PLAYLIST_AMOUNT, search_type="playlist") #dict
        playlists = response_dict['playlists']['items']
    
        for playlist in playlists:
            tracks_href = playlist["tracks"]["href"]
            headers = {'Authorization': f"Bearer {session['access_token']}"}
            tracks_response = requests.get(tracks_href, headers=headers).json()
            for item in tracks_response["items"]:
                track = item["track"]
                results.add((track['name'], track['uri']))
    return results