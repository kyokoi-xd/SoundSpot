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
            # Убираем postprocessors для конвертации в mp3
            'cookiefile': 'youtube_cookies.txt',
        }

    def download_track(self, query: str) -> str:
        with YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(f'ytsearch:{query}', download=True)
            entry = info['entries'][0] if 'entries' in info else info
            file_id = entry.get('id')
            filename = ydl.prepare_filename(entry)
            # Возвращаем оригинальный путь к файлу без изменения расширения
            return filename

youtube_client = YoutubeClient()