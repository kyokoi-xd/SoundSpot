#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы Yandex Music клиента
"""

from yandex_client import yandex_client
from config import config
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

def test_yandex_client():
    print("🔍 Тестирование Yandex Music клиента...")
    
    # Проверяем наличие токена
    if config.YANDEX_TOKEN:
        print(f"✅ Yandex токен найден: {config.YANDEX_TOKEN[:10]}...")
    else:
        print("⚠️  Yandex токен не найден в конфигурации")
    
    # Проверяем инициализацию
    if not yandex_client.is_available():
        print("❌ Yandex Music клиент недоступен")
        return False
    
    print("✅ Yandex Music клиент инициализирован")
    
    # Тестируем поиск с более простым запросом
    query = "Mozart"
    print(f"🔍 Поиск: {query}")
    
    tracks = yandex_client.search_track(query, limit=3)
    
    if not tracks:
        print("❌ Треки не найдены")
        return False
    
    print(f"✅ Найдено {len(tracks)} треков:")
    for i, track in enumerate(tracks, 1):
        title = track.get('name', 'Unknown')
        artist = track.get('artist', [{}])[0].get('name', 'Unknown')
        print(f"  {i}. {title} - {artist}")
    
    # Тестируем скачивание первого трека
    if tracks:
        print(f"\n📥 Тестирование скачивания: {tracks[0]['name']}")
        file_path = yandex_client.download_track(tracks[0])
        
        if file_path:
            print(f"✅ Трек скачан: {file_path}")
            # Удаляем тестовый файл
            import os
            if os.path.exists(file_path):
                os.remove(file_path)
                print("🧹 Тестовый файл удален")
        else:
            print("❌ Ошибка при скачивании")
            return False
    
    print("\n🎉 Все тесты пройдены успешно!")
    return True

if __name__ == "__main__":
    test_yandex_client() 