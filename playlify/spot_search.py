"""
spot_search uses the Spotify API to turn a user's context into 
songs to be used to form the user's sentence
"""

from typing import List
import requests
from constants import API_BASE_URL

def search_tracks(session, context: str, mood: str) -> List:
    """
    spot_search uses the spotify API to find songs based on the user's context

    Args:
        context: the user's context which will be used to find songs
    
    Returns: a list of songs found as tuples with the first element a song's 
    name and the second element a song's uid

    Ideas for improvement: 
        - use wildcard % character
        - play around with limit/offset more
        - TODO: add genre filter to only find songs from user's genre
    """
    def call_spot(query: str, offset: int, limit: int):
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        params = {
            "q": query,
            "offset": offset,
            "type": "track",
            "limit": limit
        }
        responses = requests.get(API_BASE_URL + 'search', headers=headers, params=params)
        responses_json = responses.json()
        tracks = responses_json['tracks']['items']
        for track in tracks:
            results.append((track['name'], track['uri']))

    results = []
    context = context.split()
    context = list(set(context)) # remove duplicates

    mood = mood.split()
    for word in mood:
        call_spot(query=word, offset=5, limit=5)
        
    # call API with individual words
    for word in context:
        call_spot(query=word, offset=5, limit=5)

    # try coupling up words
    for i in range(len(context) - 1):
        call_spot(query=context[i] + " " + context[i + 1], offset=0, limit=2)

    return results
