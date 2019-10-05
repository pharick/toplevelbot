from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from ..api import Api
from ..settings import separator

NUMBER, BEAUTY, COLOR, SHAPE = range(4)
marks_choices = [['0', '1', '2'],
                 ['3', '4', '5'],
                 ['6', '7', '8'],
                 ['9', '10', '/cancel']]

mark_range_reply = 'Оценка дожна быть от 0 до 10. Пожалуйста, запустите команду /rate заново.'


def check_mark(mark):
    return 10 >= mark >= 0


def make_participant_choices(participants, line_len):
    count = 0
    line = -1
    participant_choices = []

    for participant in participants.keys():
        if count % line_len == 0:
            line += 1
            participant_choices.append([])

        participant_choices[line].append(str(participant))
        count += 1

    return participant_choices


def send_participant_notification(bot, participant_id, judge_name, marks):
    participant_session = Api.get(f'participant-sessions/{participant_id}')

    if participant_session.status_code != 200:
        return

    chat_id = participant_session.json()['chat_id']

    participant_notification_message = f'Вас оценил судья {judge_name}.\n' \
                                       f'{separator}\n' \
                                       f'*Красота:* {marks["beauty"]}\n' \
                                       f'*Цвет:* {marks["color"]}\n' \
                                       f'*Форма:* {marks["shape"]}\n'

    bot.send_message(chat_id, participant_notification_message, ParseMode.MARKDOWN)


def rate(update, context):
    if not context.user_data['is_judge']:
        return ConversationHandler.END

    judge = context.user_data['judge']
    participants = Api.get('participants').json()
    ratings = Api.get('ratings', {'judge': judge['id']}).json()

    rated_participants = [rating['participant'] for rating in ratings]
    participants = {participant['number']: participant for participant in participants
                    if participant['id'] not in rated_participants}

    context.user_data['participants'] = participants
    participant_choices = make_participant_choices(participants, 3)

    update.message.reply_text(
        'Вы собираетесь оценить участника.\n'
        'Сначала выберите его номер.',
        reply_markup=ReplyKeyboardMarkup(participant_choices, one_time_keyboard=True)
    )

    return NUMBER


def number(update, context):
    participants = context.user_data['participants']
    participant_number = int(update.message.text)

    if participant_number not in participants.keys():
        update.message.reply_text(
            f'Участника #{participant_number} нет или вы уже оценили его.\n'
            'Пожалуйста, запустите команду /rate заново.',
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    context.chat_data['participant'] = participants[participant_number]
    context.chat_data['marks'] = {}

    update.message.reply_markdown(
        f'*Оцениваем участника #{participant_number}*\n'
        f'{separator}\n'
        'Оцените красоту.',
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
        f'*Оцениваем участника #{participant["number"]}*\n'
        f'{separator}\n'
        f'*Красота:* {marks["beauty"]}\n'
        f'{separator}\n'
        'Оцените цвет.',
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
        f'*Оцениваем участника #{participant["number"]}*\n'
        f'{separator}\n'
        f'*Красота:* {marks["beauty"]}\n'
        f'*Цвет:* {marks["color"]}\n'
        f'{separator}\n'
        'Оцените форму.',
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
        f'*Вы оценили участника #{participant["number"]}*\n'
        f'{separator}\n'
        f'*Красота:* {marks["beauty"]}\n'
        f'*Цвет:* {marks["color"]}\n'
        f'*Форма:* {marks["shape"]}\n',
        reply_markup=ReplyKeyboardRemove()
    )

    judge_name = f'{judge["first_name"]} {judge["last_name"]}'
    send_participant_notification(context.bot, participant['id'], judge_name, marks)

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_markdown('Вы отменили оценку участника.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


rateConversationHandler = ConversationHandler(
    entry_points=[CommandHandler('rate', rate)],

    states={
        NUMBER: [MessageHandler(Filters.regex(r'\d+'), number)],
        BEAUTY: [MessageHandler(Filters.regex(r'\d+'), beauty)],
        COLOR: [MessageHandler(Filters.regex(r'\d+'), color)],
        SHAPE: [MessageHandler(Filters.regex(r'\d+'), shape)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
