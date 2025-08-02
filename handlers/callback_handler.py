from telegram import Update
from telegram.ext import ContextTypes
import threading
from yandex_client import yandex_client
import os

user_playback = {}
user_playback_lock = threading.Lock()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 🎯 ШАГ 1: Получаем данные из callback
    query = update.callback_query
    await query.answer()  # Убираем "часики" у кнопки

    user_id = query.from_user.id
    idx = int(query.data)

    # 🔒 ШАГ 2: Безопасно получаем треки пользователя
    with user_playback_lock:
        tracks = user_playback.get(user_id, [])

    # ❌ ШАГ 3: Проверяем валидность индекса
    if idx < 0 or idx >= len(tracks):
        await query.edit_message_text("❌ Неверный индекс трека.")
        return

    # 🎵 ШАГ 4: Получаем информацию о треке
    track = tracks[idx]
    title = track.get('name', 'Unknown')
    artist = track.get('artist', [{}])[0].get('name', 'Unknown')

    # ⏳ ШАГ 5: Отправляем статус загрузки
    status_message = await query.edit_message_text("⏳ Скачиваю трек из Yandex Music...")
    
    try:
        # 📥 ШАГ 6: Скачиваем трек через Yandex
        file_path = yandex_client.download_track(track)
        
        if not file_path or not os.path.exists(file_path):
            await status_message.edit_text("❌ Ошибка при скачивании трека из Yandex Music.")
            return
        
        # 🎵 ШАГ 7: Отправляем аудио с красивым caption
        caption = f"🎵 {title} - {artist}\n📱 Скачано из Yandex Music"
        try:
            with open(file_path, 'rb') as f:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=f,
                    caption=caption,
                    title=title,
                    performer=artist
                )
        finally:
            # 🧹 ШАГ 8: Удаляем временный файл
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # ✅ ШАГ 9: Удаляем статусное сообщение
        await status_message.delete()
        
    except Exception as e:
        # ❌ ШАГ 10: Обработка ошибок
        await status_message.edit_text(f"❌ Ошибка при загрузке трека: {str(e)}")