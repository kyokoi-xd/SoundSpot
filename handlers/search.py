from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from spotify_client import spotify_client
from handlers.callback_handler import user_playback

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        query = ' '.join(context.args)
    else:
        query = update.message.text.strip() if update.message.text else ''

    if not query:
        await update.message.reply_text("Пожалуйста, укажи поисковый запрос")
        return
    
    tracks = spotify_client.search_tracks(query)
    if not tracks:
        return await update.message.reply_text("Ничего не найдено.")

    user_playback[update.effective_user.id] = tracks
    
    buttons = [[InlineKeyboardButton(f"{i+1}. {t.get('name')} - {t['artists'][0].get('name')}", callback_data=str(i))] for i, t in enumerate(tracks)]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(f"Результаты поиска:", reply_markup=markup)