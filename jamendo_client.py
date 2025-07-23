import requests
from config import config

class JamendoClient:
    BASE_URL = 'https://api.jamendo.com/v3.0'

    def __init__(self):
        self.client_id = config.JAMENDO_CLIENT_ID

    def search_tracks(self, query: str, limit: int = 10):
        """Search for tracks on Jamendo."""
        url = f'{self.BASE_URL}/tracks'
        params = {
            'client_id': self.client_id,
            'format': 'json',
            'limit': limit,
            'search': query
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get('results', [])
    
jamendo_client = JamendoClient()