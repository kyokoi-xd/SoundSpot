from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from config import config

class SpotifyClient:
    def __init__(self):
        auth_manager = SpotifyClientCredentials(
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET
        )
        self.client = Spotify(auth_manager=auth_manager)

    def search_tracks(self, query: str, limit: int = 10):
        "Search for tracks on Spotify."
        results = self.client.search(q=query, type='track', limit=limit)
        return results.get('tracks', {}).get('items', [])
        
spotify_client = SpotifyClient()