import requests
from constants import API_BASE_URL
from typing import Set

def collect_songs(session, mood: str) -> set:
    results = set()
    mood = mood.split()
    for word in mood:
        mood_results = call_spot(session, query=word, offset=0, limit=5)
        results.update(mood_results)
    return results # testing purposes

def call_spot(session, query: str, offset: int, limit: int) -> Set:
    results = set()
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    params = {
        "q": query,
        "offset": offset,
        "type": "playlist",
        "limit": limit # max amount of playlists to retrieve
    }
    responses = requests.get(API_BASE_URL + 'search', headers=headers, params=params)
    responses_json = responses.json()
    playlists = responses_json['playlists']['items']
    for playlist in playlists:
        tracks_href = playlist["tracks"]["href"]
        track_set = retrieve_tracks(tracks_url=tracks_href, headers=headers)
        results.update(track_set)
    return results

def retrieve_tracks(tracks_url: str, headers: dict) -> Set:
    results = set()
    # Make a request to get the tracks from the playlist
    response = requests.get(tracks_url, headers=headers)
    response_json = response.json()
    for item in response_json["items"]:
        track = item["track"]
        results.add((track['name'], track['uri']))
    return results