from typing import List
import requests
from constants import API_BASE_URL, NUM_SONGS

def spot_search(session, context: str) -> List:
    """
    spot_search uses the spotify API to find songs based on the user's context

    Args:
        context: the user's context which will be used to find songs
    
    Returns: a list of songs found including their URI's
    """
    results = []

    context = context.split()
    for word in context:
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        params = {
            "q": word, # TODO (suze) at genre filter to only find songs from user's genre
            "type": "track",
            "limit": NUM_SONGS
        }
        # TODO: (suze) make it so that spotify only finds titles as close to the input word as possible
        
        responses = requests.get(API_BASE_URL + 'search', headers=headers, params=params)
        responses_json = responses.json()
        tracks = responses_json['tracks']['items']
        for track in tracks:
            results.append((track['name'], track['uri']))
    return results

