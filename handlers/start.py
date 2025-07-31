from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start - приветствует пользователя и объясняет как пользоваться ботом
    """
    welcome_text = (
        "🎵 **Добро пожаловать в SoundSpot!**\n\n"
        "Я помогу вам найти и скачать любую музыку.\n\n"
        "**Как пользоваться:**\n"
        "• Просто напишите название трека или исполнителя\n"
        "• Или используйте команду /search <название>\n"
        "• Выберите трек из списка и получите аудиофайл\n\n"
        "**Примеры:**\n"
        "• `Queen Bohemian Rhapsody`\n"
        "• `Ed Sheeran Shape of You`\n"
        "• `/search The Beatles`\n\n"
        "🎧 **Начните поиск прямо сейчас!**"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown') 