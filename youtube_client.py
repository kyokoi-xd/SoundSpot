import os
import uuid
from yt_dlp import YoutubeDL
from config import config

class YoutubeClient:
    def __init__(self):
        self.ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def download_track(self, query: str) -> str:
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{query}', download=True)
            entry = info['entries'][0] if 'entries' in info else info
            file_id = entry.get('id')
            filename = ydl.prepare_filename(entry)
            base, _ = os.path.splitext(filename)
            return f'{base}.mp3'

youtube_client = YoutubeClient()