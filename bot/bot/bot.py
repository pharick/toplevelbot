import logging
from telegram.ext import Updater, PicklePersistence


class Bot:
    def __init__(self, token):
        self.persistence = PicklePersistence(filename='bot_persistence')
        self.updater = Updater(token, persistence=self.persistence, use_context=True)

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

    def add_handler(self, handler):
        self.updater.dispatcher.add_handler(handler)

    def loop(self):
        self.updater.start_polling()
        self.updater.idle()
