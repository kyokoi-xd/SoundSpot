from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from spotify_client import spotify_client
from jamendo_client import jamendo_client

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
    
    buttons = []
    for t in tracks:
        title = t.get('name') or t.get('name')
        artist = (t.get('artists')[0]['name'] if source == 'Spotify' else t.get('artist_name'))
        url = t.get('external_urls', {}).get('spotify') if source == 'Spotify' else t.get('audio')
        buttons.append([InlineKeyboardButton(f"{title} - {artist}", url=url)])

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Результаты поиска {source}:", reply_markup=reply_markup)