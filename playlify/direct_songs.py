"""
spot_search uses the Spotify API to turn a user's context into 
songs to be used to form the user's sentence
"""

from typing import Set
from .constants import API_BASE_URL, TRACK_AMOUNT, TRACK_INDIVIDUAL_OFFSET, TRACK_COUPLED_OFFSET
from .utils import search_spotify

def collect_API_songs(session, context: str, mood: str) -> Set:
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
    def query_and_process(session, query: str, offset: int, limit: int):
        response = search_spotify(session, query=query, offset=offset, limit=limit, search_type="track")
        tracks = response['tracks']['items']
        for track in tracks:
            results.add((track['name'], track['uri']))

    results = set()
    
    # call API with individual words from mood
    query_and_process(session, query=mood, offset=TRACK_INDIVIDUAL_OFFSET, limit=TRACK_AMOUNT)
    
    # call API with individual words from context
    context = context.split()
    context = list(set(context)) # remove duplicates
    for word in context:
        query_and_process(session, query=word, offset=TRACK_INDIVIDUAL_OFFSET, limit=TRACK_AMOUNT)

    # call API with coupled words from context
    for i in range(len(context) - 1):
        query_and_process(session, query=context[i] + " " + context[i + 1], offset=TRACK_COUPLED_OFFSET, limit=TRACK_AMOUNT)

    return results
