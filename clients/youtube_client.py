import os
import uuid
from yt_dlp import YoutubeDL
from config import config

class YoutubeClient:
    def __init__(self):
        self.ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'bestaudio[ext=m4a]/bestaudio/best',  # Скачиваем m4a если возможно
            'quiet': True,
            'noplaylist': True,
            'cookiefile': 'youtube_cookies.txt',
        }

    def download_track(self, query: str) -> str:
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{query}', download=True)
            entry = info['entries'][0] if 'entries' in info else info
            filename = ydl.prepare_filename(entry)
            return filename

youtube_client = YoutubeClient()