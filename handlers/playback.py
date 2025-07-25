from telegram import Update
from telegram.ext import ContextTypes
from spotify_client import spotify_client
from jamendo_client import jamendo_client

import threading

user_playback = {}
user_playback_lock = threading.Lock()

async def play_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    args = context.args

    if not args or not args[0].isdigit():
        await update.message.reply_text("Укажи номер трека: /play <номер>")
        return

    track_number = int(args[0])
    if track_number < 1:
        await update.message.reply_text("Номер трека должен быть больше 0.")
        return

    index = track_number - 1

    with user_playback_lock:
        last_search = user_playback.get(user_id, {}).get('tracks', [])
        source = user_playback.get(user_id, {}).get('source')

    if not last_search:
        await update.message.reply_text("Сначала нужно выполнить поиск: /search <запрос>")
        return

    if index < 0 or index >= len(last_search):
        await update.message.reply_text("Неверный номер трека.")
        return

    track = last_search[index]
    if source == 'Spotify':
        url = track.get('preview_url')
        artist_name = track.get('artists', [{}])[0].get('name', 'Unknown Artist')
    else:
        url = track.get('audio')
        artist_name = track.get('artist_name', 'Unknown Artist')

    with user_playback_lock:
        user_playback[user_id] = {'tracks': last_search, 'source': source, 'current_index': index}

    caption = f"▶️ Воспроизведение: {track.get('name')} - {artist_name}"

    if url:
        await update.message.reply_audio(audio=url, caption=caption)
    else:
        await update.message.reply_text("Нет доступного аудиофайла для этого трека.")