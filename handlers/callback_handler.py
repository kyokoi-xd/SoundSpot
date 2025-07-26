from telegram import Update
from telegram.ext import ContextTypes
import threading
from config import config

user_playback = {}
user_playback_lock = threading.Lock()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    idx = int(query.data)

    with user_playback_lock:
        state = user_playback.get(user_id, {})

    tracks = state.get('tracks', [])
    source = state.get('source')

    if idx < 0 or idx >= len(tracks):
        await query.edit_message_text("Неверный индекс трека.")
        return

    track = tracks[idx]

    if source == 'Spotify':
        url = track.get('preview_url')
        artists = track['artists'][0]['name']
    else:
        url = track.get('audio')
        artists = track.get('artist_name')

    caption = f"▶️ Воспроизведение: {track.get('name')} - {artists}"

    if url:
        await context.bot.send_audio(chat_id=query.message.chat_id, audio=url, caption=caption)
    else:
        await query.edit_message_text("Нет доступного аудио для воспроизведения.")