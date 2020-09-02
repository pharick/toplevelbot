import bot.handlers as handlers
from bot import Bot

from bot.conversation_handlers import rateConversationHandler, doctorRateConversationHandler


def main():
    token = '881682371:AAE6aXri7GrTvdIxkUf2e7Ii98xtVzNgnu0'

    bot = Bot(token)

    bot.add_handler(handlers.startHandler)
    bot.add_handler(rateConversationHandler)
    bot.add_handler(doctorRateConversationHandler)

    bot.loop()


if __name__ == "__main__":
    main()
