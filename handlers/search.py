from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from spotify_client import spotify_client
from youtube_client import youtube_client
from handlers.callback_handler import user_playback

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Пожалуйста, укажи поисковый запрос: /search <название или артист>")
        return
    
    tracks = spotify_client.search_tracks(query)
    source = 'Spotify'
    if not tracks:
        tracks = [{'name': 'query', 'source_query': query}]
        source = 'YouTube'
    
    user_playback[update.effective_user.id] = {
        'tracks': tracks,
        'source': source,
    }

    buttons = []
    for i, t in enumerate(tracks):
        if source == 'Spotify':
            title = t.get('name')
            artist = t['artists'][0]['name']
        else:
            title = t.get('name')
            artist = ''
        buttons.append([InlineKeyboardButton(f"{i+1}. {title} - {artist}", callback_data=str(i))])
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Результаты поиска {source}:", reply_markup=markup)