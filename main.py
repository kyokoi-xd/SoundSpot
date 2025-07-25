import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import config
from handlers.search import search_handler
from utils.logger import setup_logger


setup_logger()
logger = logging.getLogger(__name__)

application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

application.add_handler(CommandHandler('search', search_handler))

if __name__ == "__main__":
    logger.info('Bot started (Long Polling)')
    application.run_polling()