from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from ..api import fetch_api

NUMBER, BEAUTY, COLOR, SHAPE = range(4)
marks_choices = [str(i) for i in range(0, 11)]


def mark(update, context):  # TODO: сделать restricted декоратор
    if not context.user_data['is_judge']:
        return ConversationHandler.END

    participants = fetch_api('participants')
    participant_numbers = [str(participant['number']) for participant in participants]

    update.message.reply_text(
        'Вы собираетесь оценить участника.\n'
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup([participant_numbers], one_time_keyboard=True)
    )

    return NUMBER


def number(update, context):
    participants = fetch_api('participants')
    participant_numbers = [str(participant['number']) for participant in participants]
    participant_number = update.message.text

    if participant_number not in participant_numbers:
        update.message.reply_text(
            'Участника с номером {} нет.'.format(participant_number),
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    context.chat_data['participant_number'] = participant_number
    context.chat_data['marks'] = {}

    update.message.reply_text(
        'Вы оцениваете участника с номером {}.\n'
        'Оцените красоту.'.format(participant_number),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return BEAUTY


def beauty(update, context):
    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['beauty'] = update.message.text

    update.message.reply_text(
        'Вы оцениваете участника с номером {}.\n'
        'Ваша оценка за красоту: {}.\n'
        'Оцените цвет.'
        .format(participant_number, marks['beauty']),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return COLOR


def color(update, context):
    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['color'] = update.message.text

    update.message.reply_text(
        'Вы оцениваете участника с номером {}.\n'
        'Ваша оценка за красоту: {}.\n'
        'Ваша оценка за цвет: {}.\n'
        'Оцените форму.'.format(participant_number, marks['beauty'], marks['color']),
        reply_markup=ReplyKeyboardMarkup([marks_choices])
    )

    return SHAPE


def shape(update, context):
    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['shape'] = update.message.text

    update.message.reply_text(
        'Вы оцениваете участника с номером {}.\n'
        'Ваша оценка за красоту: {}.\n'
        'Ваша оценка за цвет: {}.\n'
        'Ваша оценка за форму: {}.\n'
        'Вы полностью оценили участника.'.format(participant_number, marks['beauty'], marks['color'], marks['shape']),
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
