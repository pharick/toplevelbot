import os
import bot.handlers as handlers
from bot import Bot

from bot.conversation_handlers import rateConversationHandler, doctorRateConversationHandler


def main():
    token = os.environ.get('TOKEN')

    bot = Bot(token)

    bot.add_handler(handlers.startHandler)
    bot.add_handler(rateConversationHandler)
    bot.add_handler(doctorRateConversationHandler)

    bot.loop()


if __name__ == "__main__":
    main()
