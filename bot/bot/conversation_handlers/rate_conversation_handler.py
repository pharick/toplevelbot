from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from ..api import fetch_api

NUMBER, BEAUTY, COLOR, SHAPE = range(4)
marks_choices = [['0', '1', '2'],
                 ['3', '4', '5'],
                 ['6', '7', '8'],
                 ['9', '10']]

mark_range_reply = 'Оценка дожна быть от 0 до 10. Пожалуйста, запустите команду /rate заново.'


def check_mark(mark):
    return 10 >= mark >= 0


def rate(update, context):  # TODO: сделать restricted декоратор
    if not context.user_data['is_judge']:
        return ConversationHandler.END

    participants = fetch_api('participants')
    participant_numbers = [[str(participant['number'])] for participant in participants]

    update.message.reply_text(
        'Вы собираетесь оценить участника.\n'
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup(participant_numbers, one_time_keyboard=True)
    )

    return NUMBER


def number(update, context):
    participants = fetch_api('participants')
    participant_numbers = [str(participant['number']) for participant in participants]
    participant_number = update.message.text

    if participant_number not in participant_numbers:
        update.message.reply_text(
            'Участника с номером {} нет.'
            'Пожалуйста, запустите команду /rate заново.'
            .format(participant_number),
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    context.chat_data['participant_number'] = participant_number
    context.chat_data['marks'] = {}

    update.message.reply_markdown(
        '*Оцениваем участника:* {}\n'
        '----------\n'
        'Оцените красоту.'
        .format(participant_number),
        reply_markup=ReplyKeyboardMarkup(marks_choices)
    )

    return BEAUTY


def beauty(update, context):
    mark = int(update.message.text)

    if not check_mark(mark):
        update.message.reply_text(mark_range_reply)
        return ConversationHandler.END

    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['beauty'] = mark

    update.message.reply_markdown(
        '*Оцениваем участника:* {}\n'
        '----------\n'
        '*Красота:* {}\n'
        '----------\n'
        'Оцените цвет.'
        .format(participant_number, marks['beauty']),
        reply_markup=ReplyKeyboardMarkup(marks_choices)
    )

    return COLOR


def color(update, context):
    mark = int(update.message.text)

    if not check_mark(mark):
        update.message.reply_text(mark_range_reply)
        return ConversationHandler.END

    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['color'] = mark

    update.message.reply_markdown(
        '*Оцениваем участника:* {}\n'
        '----------\n'
        '*Красота:* {}\n'
        '*Цвет:* {}\n'
        '----------\n'
        'Оцените форму.'
        .format(participant_number, marks['beauty'], marks['color']),
        reply_markup=ReplyKeyboardMarkup(marks_choices)
    )

    return SHAPE


def shape(update, context):
    mark = int(update.message.text)

    if not check_mark(mark):
        update.message.reply_text(mark_range_reply)
        return ConversationHandler.END

    participant_number = context.chat_data['participant_number']
    marks = context.chat_data['marks']
    marks['shape'] = mark

    update.message.reply_markdown(
        '*Вы полностью оценили участника:* {}\n'
        '----------\n'
        '*Красота:* {}\n'
        '*Цвет:* {}\n'
        '*Форма:* {}\n'
        .format(participant_number, marks['beauty'], marks['color'], marks['shape']),
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


rateConversationHandler = ConversationHandler(
    entry_points=[CommandHandler('rate', rate)],

    states={
        NUMBER: [MessageHandler(Filters.regex(r'\d+'), number)],
        BEAUTY: [MessageHandler(Filters.regex(r'\d+'), beauty)],
        COLOR: [MessageHandler(Filters.regex(r'\d+'), color)],
        SHAPE: [MessageHandler(Filters.regex(r'\d+'), shape)],
    },

    fallbacks=[]
)
