from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from spotify_client import spotify_client
from jamendo_client import jamendo_client
from handlers.callback_handler import user_playback

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Пожалуйста, укажи поисковый запрос: /search <название или артист>")
        return
    
    tracks = spotify_client.search_tracks(query)
    source = 'Spotify'
    if not tracks:
        tracks = jamendo_client.search_tracks(query)
        source = 'Jamendo'

    if not tracks:
        await update.message.reply_text("Ничего не найдено.")
        return
    
    user_playback[update.effective_user.id] = {
        'tracks': tracks,
        'source': source,
    }

    buttons = [
        [InlineKeyboardButton(f"{i+1}. {t.get('name')} - "
                              f"{t['artists'][0]['name'] if source == 'Spotify' else t.get('artist_name')}",
                              callback_data=str(i))]
        for i, t in enumerate(tracks)
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Результаты поиска {source}:", reply_markup=reply_markup)