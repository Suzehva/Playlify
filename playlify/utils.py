import requests
from typing import Dict
from constants import API_BASE_URL

def search_spotify(session, query: str, offset: int, limit: int, search_type: str) -> Dict:
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        params = {
            "q": query,
            "offset": offset,
            "type": search_type,
            "limit": limit
        }
        response = requests.get(API_BASE_URL + 'search', headers=headers, params=params).json()
        return response
