import bot.handlers as handlers
from bot import Bot

from bot.conversation_handlers import rateConversationHandler


def main():
    token = ''

    bot = Bot(token)

    bot.add_handler(handlers.startHandler)
    bot.add_handler(rateConversationHandler)

    bot.loop()


if __name__ == "__main__":
    main()
