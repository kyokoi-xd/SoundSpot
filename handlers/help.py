from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /help - показывает подробную справку
    """
    help_text = (
        "📚 **Справка по SoundSpot**\n\n"
        "**🔍 Поиск музыки:**\n"
        "• Напишите название трека или исполнителя\n"
        "• Используйте команду `/search <название>`\n\n"
        "**🎵 Как скачать трек:**\n"
        "1. Найдите нужный трек в списке\n"
        "2. Нажмите на кнопку с номером трека\n"
        "3. Дождитесь загрузки (⏳)\n"
        "4. Получите аудиофайл в чат\n\n"
        "**💡 Советы:**\n"
        "• Используйте точные названия для лучшего поиска\n"
        "• Можно искать по исполнителю: `Queen`\n"
        "• Или по названию трека: `Bohemian Rhapsody`\n\n"
        "**❓ Примеры запросов:**\n"
        "• `The Beatles`\n"
        "• `Ed Sheeran Shape of You`\n"
        "• `Queen Bohemian Rhapsody`\n\n"
        "**🆘 Если что-то не работает:**\n"
        "• Попробуйте другой запрос\n"
        "• Проверьте правильность написания\n"
        "• Обратитесь к администратору\n\n"
        "🎧 **Приятного прослушивания!**"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown') 