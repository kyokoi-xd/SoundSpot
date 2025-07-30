from telegram import Update
from telegram.ext import ContextTypes
import threading
from youtube_client import youtube_client
import os

user_playback = {}
user_playback_lock = threading.Lock()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    idx = int(query.data)

    with user_playback_lock:
        tracks = user_playback.get(user_id, [])

    if idx < 0 or idx >= len(tracks):
        await query.edit_message_text("Неверный индекс трека.")
        return

    track = tracks[idx]
    title = track.get('name')
    artist = track.get('artists')[0].get('name')
    search_query = f"{title} {artist}"

    file_path = youtube_client.download_track(search_query)
    caption = f"▶️ Воспроизведение: {title}"
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
        if os.path.exists(file_path):
            os.remove(file_path)