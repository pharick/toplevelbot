import json
import requests

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

PARTICIPANT, BEAUTY, COLOR, SHAPE = range(4)

api_url_base = 'http://127.0.0.1:8000/api/'

headers = {
    'Content-Type': 'application/json',
}

api_url = '{}profiles'.format(api_url_base)
response = requests.get(api_url, headers=headers)
profiles = json.loads(response.content.decode('utf-8'))

profilesChoices = [str(profile['participant_number']) for profile in profiles]
marksChoices = [str(i) for i in range(0, 11)]


def mark(bot, update):
    update.message.reply_text(
        'Вы собираетесь оценить участника. '
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup([profilesChoices], one_time_keyboard=True)
    )

    return PARTICIPANT


def participant(bot, update):
    participant_number = update.message.text

    print(profilesChoices, participant_number)

    if participant_number not in profilesChoices:
        update.message.reply_text(
            'Участника с таким номером нет.',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Вы оцениваете участника с номером {}. '
            'Оцените красоту.'.format(participant_number),
            reply_markup=ReplyKeyboardMarkup([marksChoices])
        )

    return BEAUTY


def beauty(bot, update):
    mark = update.message.text

    update.message.reply_text(
        'Ваша оценка за красоту: {}. '
        'Оцените цвет.'.format(mark),
        reply_markup=ReplyKeyboardMarkup([marksChoices])
    )

    return COLOR


def color(bot, update):
    mark = update.message.text

    update.message.reply_text(
        'Ваша оценка за цвет: {}. '
        'Оцените форму.'.format(mark),
        reply_markup=ReplyKeyboardMarkup([marksChoices])
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
        PARTICIPANT: [MessageHandler(Filters.regex(r'\d+'), participant)],
        BEAUTY: [MessageHandler(Filters.regex(r'\d+'), beauty)],
        COLOR: [MessageHandler(Filters.regex(r'\d+'), color)],
        SHAPE: [MessageHandler(Filters.regex(r'\d+'), shape)],
    },

    fallbacks=[]
)
