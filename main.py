import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import config
from handlers.search import search_handler
from handlers.callback_handler import callback_handler
from handlers.start import start_handler
from handlers.help import help_handler
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

# 🎯 Добавляем обработчики команд
application.add_handler(CommandHandler('start', start_handler))  # Приветствие
application.add_handler(CommandHandler('help', help_handler))    # Справка
application.add_handler(CommandHandler('search', search_handler))  # Поиск
application.add_handler(CallbackQueryHandler(callback_handler))  # Кнопки
# Новый обработчик для любого текста
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))

if __name__ == "__main__":
    logger.info('Bot started (Long Polling)')
    application.run_polling()