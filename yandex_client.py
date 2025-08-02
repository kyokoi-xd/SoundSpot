import logging
from typing import List, Dict, Any, Optional
from yandex_music import Client
from io import BytesIO
import requests
import os
import tempfile
from config import config


logger = logging.getLogger(__name__)


class YandexMusicClient:
    def __init__(self):
        self.client = None
        self.init_client()

    def init_client(self):
        try:
            # Используем токен для аутентификации
            if config.YANDEX_TOKEN:
                self.client = Client(config.YANDEX_TOKEN).init()
                logger.info("Yandex Music client initialized with token")
            else:
                # Попытка инициализации без токена (может не работать)
                self.client = Client().init()
                logger.info("Yandex Music client initialized without token")
        except Exception as e:
            logger.error(f"Error initializing Yandex Music client: {e}")
            self.client = None

    def search_track(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.client:
            logger.warning("Yandex Music client not initialized")
            return []

        try:
            # Пробуем разные варианты поиска
            search_queries = [query]
            
            # Если запрос содержит название и артиста, пробуем только название
            if ' - ' in query:
                title_only = query.split(' - ')[0].strip()
                search_queries.append(title_only)
            
            # Если запрос длинный, пробуем короткую версию
            if len(query) > 20:
                short_query = ' '.join(query.split()[:3])
                search_queries.append(short_query)

            for search_query in search_queries:
                try:
                    logger.info(f"Trying search query: {search_query}")
                    search_result = self.client.search(search_query, type_="track")
                    tracks = search_result.tracks.results[:limit]

                    if tracks:
                        enriched_tracks = []
                        for track in tracks:
                            enriched_track = {
                                'name': track.title,
                                'artist': [{'name': artist.name} for artist in track.artists],
                                'yandex_id': track.id,
                                'source': 'Yandex',
                                'source_query': f"{track.title} {' '.join([artist.name for artist in track.artists])}"
                            }
                            enriched_tracks.append(enriched_track)

                        logger.info(f"Found {len(enriched_tracks)} tracks for query: {search_query}")
                        return enriched_tracks
                        
                except Exception as e:
                    logger.warning(f"Search failed for query '{search_query}': {e}")
                    continue

            logger.warning(f"No tracks found for any search query")
            return []
            
        except Exception as e:
            logger.error(f"Error searching tracks: {e}")
            return []
        
    def get_track_audio(self, track_info: Dict[str, Any]) -> Optional[BytesIO]:
        if not self.client:
            return None
        
        try:
            track_id = track_info.get('yandex_id')
            if not track_id:
                return None

            track = self.client.tracks([track_id])[0]
            download_info = track.get_download_info()

            if not download_info:
                logger.warning(f"No download info found for track: {track_id}")
                return None

            best_quality = max(download_info, key=lambda x: x.bitrate_in_kbps)
            download_url = best_quality.get_direct_link()

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            audio_buffer = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                audio_buffer.write(chunk)

            audio_buffer.seek(0)
            logger.info(f"Downloaded track audio for: {track_info['name']}")
            return audio_buffer
        except Exception as e:
            logger.error(f"Error downloading track audio: {e}")
            return None

    def download_track(self, track_info: Dict[str, Any]) -> Optional[str]:
        """
        Скачивает трек и сохраняет его во временный файл
        Возвращает путь к файлу или None в случае ошибки
        """
        if not self.client:
            logger.warning("Yandex Music client not initialized")
            return None
        
        try:
            # Создаем папку downloads если её нет
            downloads_dir = 'downloads'
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
                logger.info(f"Created downloads directory: {downloads_dir}")
            
            track_id = track_info.get('yandex_id')
            if not track_id:
                logger.warning("No yandex_id in track_info")
                return None

            track = self.client.tracks([track_id])[0]
            download_info = track.get_download_info()

            if not download_info:
                logger.warning(f"No download info found for track: {track_id}")
                return None

            # Выбираем лучшее качество
            best_quality = max(download_info, key=lambda x: x.bitrate_in_kbps)
            download_url = best_quality.get_direct_link()

            # Создаем временный файл
            temp_file = tempfile.NamedTemporaryFile(
                suffix='.mp3', 
                delete=False,
                dir=downloads_dir
            )
            file_path = temp_file.name
            temp_file.close()

            # Скачиваем файл
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded track to file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading track: {e}")
            return None

    def is_available(self) -> bool:
        """Проверяет, доступен ли клиент"""
        return self.client is not None


# Создаем глобальный экземпляр клиента
yandex_client = YandexMusicClient()