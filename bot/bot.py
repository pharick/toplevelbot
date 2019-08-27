import logging
from telegram.ext import Updater

from bot.conversations.markConversation import markConversationHandler

updater = Updater('881682371:AAE6aXri7GrTvdIxkUf2e7Ii98xtVzNgnu0')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater.dispatcher.add_handler(markConversationHandler)

updater.start_polling()
updater.idle()
