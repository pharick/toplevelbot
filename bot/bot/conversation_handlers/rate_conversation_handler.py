from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from urllib import request

from ..api import Api
from ..settings import separator

CATEGORY, NUMBER, CRITERION, RESUME, COMMENT = range(5)  # Стадии оценки

# Номинации
LIPS, EYELIDS, EYEBROWS = range(3)
category_names = {LIPS: 'Акварельные губы', EYELIDS: 'Веки с растушевкой', EYEBROWS: 'Пудровые брови'}

# Критерии для номинации ГУБЫ
lips_criteria = [
    'Общее впечатление',
    'Гармоничность формы',
    'Симметрия',
    'Выбор цвета',
    'Насыщенность',
    'Оформление контура',
    'Равномерность покраса',
    'Оформление уголков',
    'Глубина введения пигмента',
    'Травматичность'
]

# Критерии для номинации РЕСНИЦЫ
eyelids_criteria = [
    'Выбор техники',
    'Гармоничность формы',
    'Симметрия',
    'Заполнение межресничного пространства',
    'Равномерность и четкость прокраса стрелок',
    'Качество прокраса внутреннего уголка глаза',
    'Качество прокраса внешнего уголка глаза',
    'Глубина введения пигмента',
    'Градиент',
    'Травматичность'
]

# Критерии для номинации БРОВИ
eyebrows_criteria = [
    'Выбор техники',
    'Гармоничность формы',
    'Симметрия',
    'Заполнение головки брови',
    'Заполнение верха тела брови',
    'Заполнение нижней части тела брови',
    'Заполнение хвоста брови',
    'Равномерность прокраса брови',
    'Градиент',
    'Травматичность'
]

# Клавиатура для выбора оценки
marks_choices = [
    [InlineKeyboardButton('0', callback_data='0'),
     InlineKeyboardButton('1', callback_data='1'),
     InlineKeyboardButton('2', callback_data='2')],
    [InlineKeyboardButton('3', callback_data='3'),
     InlineKeyboardButton('4', callback_data='4'),
     InlineKeyboardButton('5', callback_data='5')],
    [InlineKeyboardButton('Отмена', callback_data='CANCEL')]
]

# Проверка диапазона оценки
def check_mark(mark):
    return 5 >= mark >= 0


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
def send_participant_notification(bot, participant_id, judge_name, category_number, criteria, marks, message_text):
    participant_session = Api.get(f'participant-sessions/{participant_id}')

    if participant_session.status_code != 200:
        return

    chat_id = participant_session.json()['chat_id']

    message = f'Вас оценил судья *{judge_name}* в категории *{category_names[category_number]}*:\n' \
              f'{separator}\n'

    for i in range(len(marks)):
        message += f'{criteria[i]}: *{marks[i]}*\n'

    message += f'{separator}\n' \
               f'*Итого:* {sum(marks)}\n' \
               f'{separator}\n' \
               f'*Комментарий:*\n' \
               f'{message_text}'

    bot.send_message(chat_id, message, ParseMode.MARKDOWN)


def sent_participant_photos(bot, chat_id, participant_number, category_number):
    participant = Api.get('participants', args={'number': participant_number})
    if participant.status_code != 200:
        return
    participant = participant.json()[0]
    if not participant:
        return

    if category_number == LIPS:
        if participant['photo_lips_face_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_lips_face_before']), caption='Лицо с губами до')
        if participant['photo_lips_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_lips_before']), caption='Губы до')
    elif category_number == EYELIDS:
        if participant['photo_eyeline_face_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_eyeline_face_before']), caption='Лицо с веками до')
        if participant['photo_eyeline_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_eyeline_before']), caption='Веки до')
    elif category_number == EYEBROWS:
        if participant['photo_brows_face_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_brows_face_before']), caption='Лицо с бровями до')
        if participant['photo_brows_before']:
            bot.send_photo(chat_id, request.urlopen(participant['photo_brows_before']), caption='Брови до')


# 1. Начальная стадия
def rate(update, context):
    # Проверяем, что пользователь является судьей и не является доктором
    if not context.user_data['is_judge'] or context.user_data['is_doctor']:
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

    if category_number == LIPS:
        context.chat_data['criteria'] = lips_criteria
    elif category_number == EYELIDS:
        context.chat_data['criteria'] = eyelids_criteria
    else:
        context.chat_data['criteria'] = eyebrows_criteria

    # Подгружаем список участников и уже выставленные судьей оценки
    judge = context.user_data['judge']
    participants = Api.get('participants').json()
    ratings = Api.get('ratings', {'judge': judge['id'], 'category': category_number}).json()

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
    context.chat_data['marks'] = []

    category_number = context.chat_data['category']
    criteria = context.chat_data['criteria']

    sent_participant_photos(context.bot, update.effective_chat.id, participant_number, category_number)

    query.edit_message_text(
        f'Категория *{category_names[category_number]}*\n'
        f'Оцениваем участника *#{participant_number}*\n'
        f'{separator}\n'
        f'Оцените критерий *{criteria[0]}*.',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(marks_choices)
    )

    return CRITERION


def criterion(update, context):
    query = update.callback_query

    mark = int(query.data)

    participant = context.chat_data['participant']
    marks = context.chat_data['marks']
    marks.append(mark)

    category_number = context.chat_data['category']
    criteria = context.chat_data['criteria']

    message = f'Категория *{category_names[category_number]}*\n'\
              f'*Оцениваем участника #{participant["number"]}*\n' \
              f'{separator}\n'

    for i in range(len(marks)):
        message += f'*{criteria[i]}:* {marks[i]}\n'

    message += f'{separator}\n' \
               f'Оцените критерий *{criteria[len(marks)]}*.'

    query.edit_message_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(marks_choices)
    )

    if len(marks) == len(lips_criteria) - 1:
        return RESUME

    return CRITERION


def resume(update, context):
    query = update.callback_query
    mark = int(query.data)

    participant = context.chat_data['participant']
    marks = context.chat_data['marks']
    marks.append(mark)
    category_number = context.chat_data['category']
    criteria = context.chat_data['criteria']

    message = f'Категория *{category_names[category_number]}*\n'\
              f'*Вы оценили участника #{participant["number"]}*\n' \
              f'{separator}\n'

    for i in range(len(marks)):
        message += f'*{criteria[i]}:* {marks[i]}\n'

    cancel_choices = InlineKeyboardMarkup([[InlineKeyboardButton('Отмена', callback_data='CANCEL')]])

    message += f'{separator}\n'
    message += 'Оставьте участнику текстовый комментарий:\n'

    query.edit_message_text(
        message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=cancel_choices
    )

    return COMMENT

def comment(update, context):
    comment_text = update.message.text
    category_number = context.chat_data['category']
    participant = context.chat_data['participant']
    judge = context.user_data['judge']
    marks = context.chat_data['marks']
    criteria = context.chat_data['criteria']

    rating = {
        'category': category_number,
        'participant': participant['id'],
        'judge': judge['id'],
        'marks': marks,
        'message': comment_text
    }

    Api.post('ratings', rating)

    judge_name = f'{judge["first_name"]} {judge["last_name"]}'
    send_participant_notification(context.bot, participant['id'], judge_name, category_number, criteria, marks, comment_text)

    update.message.reply_markdown(
        f'Оценка участника #{participant["number"]} закончена.\n'
        'Для оценки следующего участника введите команду /rate'
    )

    return ConversationHandler.END


def cancel(update, context):
    query = update.callback_query
    query.edit_message_text('Вы отменили оценку участника.')
    return ConversationHandler.END


rateConversationHandler = ConversationHandler(
    entry_points=[CommandHandler('rate', rate)],

    states={
        CATEGORY: [CallbackQueryHandler(category, pattern=r'\d+')],
        NUMBER: [CallbackQueryHandler(number, pattern=r'\d+')],
        CRITERION: [CallbackQueryHandler(criterion, pattern=r'\d+')],
        RESUME: [CallbackQueryHandler(resume, pattern=r'\d+')],
        COMMENT: [MessageHandler(Filters.text & ~Filters.command, comment, )]
    },

    fallbacks=[CallbackQueryHandler(cancel, pattern=r'^CANCEL$')]
)
