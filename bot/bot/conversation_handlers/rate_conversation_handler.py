from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from ..api import Api

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

    participants = Api.get('participants')
    participant_numbers = [participant['number'] for participant in participants]

    participant_choices = [[str(participant_number)] for participant_number in participant_numbers]

    update.message.reply_text(
        'Вы собираетесь оценить участника.\n'
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup(participant_choices, one_time_keyboard=True)
    )

    return NUMBER


def number(update, context):
    participants = Api.get('participants')
    participant_numbers = [participant['number'] for participant in participants]
    participant_number = int(update.message.text)

    if participant_number not in participant_numbers:
        update.message.reply_text(
            'Участника #{} нет.'
            'Пожалуйста, запустите команду /rate заново.'
            .format(participant_number),
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    judge = context.user_data['judge']
    ratings = Api.get('ratings', {'judge': judge['id']})
    rated_participant_ids = [rating['participant'] for rating in ratings]

    participant = Api.get('participants', {'number': participant_number})[0]

    if participant['id'] in rated_participant_ids:
        update.message.reply_text(
            'Вы уже оценили участника #{}. Запустите команду /rate заново и выберите другого.'
            .format(participant_number),
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    context.chat_data['participant'] = Api.get('participants', {'number': participant_number})[0]
    context.chat_data['marks'] = {}

    update.message.reply_markdown(
        '*Оцениваем участника #{}*\n'
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

    participant = context.chat_data['participant']
    marks = context.chat_data['marks']
    marks['beauty'] = mark

    update.message.reply_markdown(
        '*Оцениваем участника #{}*\n'
        '----------\n'
        '*Красота:* {}\n'
        '----------\n'
        'Оцените цвет.'
        .format(participant['number'], marks['beauty']),
        reply_markup=ReplyKeyboardMarkup(marks_choices)
    )

    return COLOR


def color(update, context):
    mark = int(update.message.text)

    if not check_mark(mark):
        update.message.reply_text(mark_range_reply)
        return ConversationHandler.END

    participant = context.chat_data['participant']
    marks = context.chat_data['marks']
    marks['color'] = mark

    update.message.reply_markdown(
        '*Оцениваем участника #{}*\n'
        '----------\n'
        '*Красота:* {}\n'
        '*Цвет:* {}\n'
        '----------\n'
        'Оцените форму.'
        .format(participant['number'], marks['beauty'], marks['color']),
        reply_markup=ReplyKeyboardMarkup(marks_choices)
    )

    return SHAPE


def shape(update, context):
    mark = int(update.message.text)

    if not check_mark(mark):
        update.message.reply_text(mark_range_reply)
        return ConversationHandler.END

    participant = context.chat_data['participant']
    marks = context.chat_data['marks']
    marks['shape'] = mark

    judge = context.user_data['judge']

    rating = {
        'participant': participant['id'],
        'judge': judge['id'],
        'marks': marks,
    }

    Api.post('ratings', rating)

    update.message.reply_markdown(
        '*Вы оценили участника #{}*\n'
        '----------\n'
        '*Красота:* {}\n'
        '*Цвет:* {}\n'
        '*Форма:* {}\n'
        .format(participant['number'], marks['beauty'], marks['color'], marks['shape']),
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
