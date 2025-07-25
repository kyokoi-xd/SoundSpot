import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import config
from handlers.search import search_handler
from utils.logger import setup_logger


setup_logger()
logger = logging.getLogger(__name__)

updater = Updater(token=config.TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("search", search_handler))

if __name__ == "__main__":
    logger.info('Bot started (Long Polling)')
    updater.start_polling()
    updater.idle()