from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from urllib import request

from ..api import Api
from ..settings import separator

CATEGORY, NUMBER, MARK = range(3)  # Стадии оценки

# Номинации
LIPS, EYELIDS, EYEBROWS = range(3)
category_names = {LIPS: 'Акварельные губы', EYELIDS: 'Веки с растушевкой', EYEBROWS: 'Пудровые брови'}

# Клавиатура для выбора оценки
marks_choices = [
    [InlineKeyboardButton('-2', callback_data='-2'),
     InlineKeyboardButton('-1', callback_data='-1'),
     InlineKeyboardButton('0', callback_data='0')],
    [InlineKeyboardButton('Отмена', callback_data='CANCEL')]
]

# Проверка диапазона оценки
def check_mark(mark):
    return 0 >= mark >= -2


# Компоновка клавиатуры для выбора участника
def make_participant_choices(participants, line_len):
    count = 0
    line = -1
    participant_choices = []

    for participant in participants.keys():
        if count % line_len == 0:
            line += 1
            participant_choices.append([])

        participant_choices[line].append(InlineKeyboardButton(participant, callback_data=str(participant)))
        count += 1

    participant_choices.append([InlineKeyboardButton('Отмена', callback_data='CANCEL')])

    return InlineKeyboardMarkup(participant_choices)


# Отправка уведомления об оценке участнику
def send_participant_notification(bot, participant_id, category_number, mark):
    participant_session = Api.get(f'participant-sessions/{participant_id}')

    if participant_session.status_code != 200:
        return

    chat_id = participant_session.json()['chat_id']

    message = f'Вас оценил санитарный врач в категории *{category_names[category_number]}*\n' \
              f'{separator}\n'

    message += f'*Оценка:* {mark}\n'

    bot.send_message(chat_id, message, ParseMode.MARKDOWN)


# 1. Начальная стадия
def rate(update, context):
    # Проверяем, что пользователь является судьей и доктором
    if not context.user_data['is_judge'] or not context.user_data['is_doctor']:
        return ConversationHandler.END

    # Формируем клавиатуру для выбора номинации
    category_choices = InlineKeyboardMarkup([
        [InlineKeyboardButton('Акварельные губы', callback_data='0')],
        [InlineKeyboardButton('Веки с растушевкой', callback_data='1')],
        [InlineKeyboardButton('Пудровые брови', callback_data='2')],
        [InlineKeyboardButton('Отмена', callback_data='CANCEL')]
    ])

    update.message.reply_markdown(
        'Выберите номинацию для оценки.',
        reply_markup=category_choices
    )

    return CATEGORY


def category(update, context):
    query = update.callback_query

    category_number = int(query.data)
    context.chat_data['category'] = category_number

    # Подгружаем список участников и уже выставленные доктором оценки
    judge = context.user_data['judge']
    participants = Api.get('participants').json()
    ratings = Api.get('doctor-ratings', {'category': category_number}).json()

    # Формируем список еще не оцененных участников
    rated_participants = [rating['participant'] for rating in ratings]
    participants = {participant['number']: participant for participant in participants
                    if participant['id'] not in rated_participants}
    context.user_data['participants'] = participants

    # Проверяем, остались ли участники для оценки
    if len(participants) == 0:
        query.edit_message_text(text='Похоже вы уже оценили всех участников в этой номинации.')
        return ConversationHandler.END

    # Формируем клавиатуру для выбора участника
    participant_choices = make_participant_choices(participants, 3)

    query.edit_message_text(
        text='Выберите номер участника для оценки.',
        reply_markup=participant_choices
    )

    return NUMBER


def number(update, context):
    query = update.callback_query

    participants = context.user_data['participants']
    participant_number = int(query.data)

    context.chat_data['participant'] = participants[participant_number]
    category_number = context.chat_data['category']

    query.edit_message_text(
        f'Категория *{category_names[category_number]}*\n'
        f'Оцениваем участника *#{participant_number}*\n',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(marks_choices)
    )

    return MARK


def mark(update, context):
    query = update.callback_query
    mark_value = int(query.data)

    participant = context.chat_data['participant']
    category_number = context.chat_data['category']
    judge = context.user_data['judge']

    rating = {
        'category': category_number,
        'participant': participant['id'],
        'judge': judge['id'],
        'mark': mark_value
    }

    Api.post('doctor-ratings', rating)

    send_participant_notification(context.bot, participant['id'], category_number, mark_value)

    query.edit_message_text(
        f'Вы оценили участника #{participant["number"]}.',
        parse_mode=ParseMode.MARKDOWN
    )

    return ConversationHandler.END


def cancel(update, context):
    query = update.callback_query
    query.edit_message_text('Вы отменили оценку участника.')
    return ConversationHandler.END


doctorRateConversationHandler = ConversationHandler(
    entry_points=[CommandHandler('doctor', rate)],

    states={
        CATEGORY: [CallbackQueryHandler(category, pattern=r'\d+')],
        NUMBER: [CallbackQueryHandler(number, pattern=r'\d+')],
        MARK: [CallbackQueryHandler(mark, pattern=r'-?\d+')]
    },

    fallbacks=[CallbackQueryHandler(cancel, pattern=r'^CANCEL$')]
)
