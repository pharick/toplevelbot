from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from ..api import fetch_api

NUMBER, BEAUTY, COLOR, SHAPE = range(4)
marks_choices = [str(i) for i in range(0, 11)]


def mark(bot, update): # TODO: сделать restricted декоратор
    judges = fetch_api('judges')
    judge_usernames = [judge['telegram_username'] for judge in judges]
    username = update.message.from_user.username

    if username not in judge_usernames:
        update.message.reply_text('Вы не имеете права оценивать участников.')
        return ConversationHandler.END

    participants = fetch_api('participants')
    participant_numbers = [str(participant['number']) for participant in participants]

    update.message.reply_text(
        'Вы собираетесь оценить участника. '
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup([participant_numbers], one_time_keyboard=True)
    )

    return NUMBER


def number(bot, update):
    participants = fetch_api('participants')
    participant_numbers = [str(participant['number']) for participant in participants]
    participant_number = update.message.text

    if participant_number not in participant_numbers:
        update.message.reply_text(
            'Участника с номером {} нет.'.format(participant_number),
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    update.message.reply_text(
        'Вы оцениваете участника с номером {}. '
        'Оцените красоту.'.format(participant_number),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return BEAUTY


def beauty(bot, update):
    mark = update.message.text

    update.message.reply_text(
        'Ваша оценка за красоту: {}. '
        'Оцените цвет.'.format(mark),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return COLOR


def color(bot, update):
    mark = update.message.text

    update.message.reply_text(
        'Ваша оценка за цвет: {}. '
        'Оцените форму.'.format(mark),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return SHAPE


def shape(bot, update):
    mark = update.message.text

    update.message.reply_text(
        'Ваша оценка за форму: {}. '
        'Вы полностью оценили участника.'.format(mark),
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


markConversationHandler = ConversationHandler(
    entry_points=[CommandHandler('mark', mark)],

    states={
        NUMBER: [MessageHandler(Filters.regex(r'\d+'), number)],
        BEAUTY: [MessageHandler(Filters.regex(r'\d+'), beauty)],
        COLOR: [MessageHandler(Filters.regex(r'\d+'), color)],
        SHAPE: [MessageHandler(Filters.regex(r'\d+'), shape)],
    },

    fallbacks=[]
)
