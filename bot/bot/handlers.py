from telegram.ext import CommandHandler
from .api import Api
from .settings import separator


def start(update, context):
    # пытаемся получить из базы данных записи судьи и участника
    username = update.message.from_user.username
    judge = Api.get(f'judges/{username}')
    participant = Api.get(f'participants/{username}')

    # проверяем, является ли пользователь судьей или участником
    if judge.status_code == 200:
        context.user_data['is_judge'] = True
        context.user_data['judge'] = judge.json()
        context.user_data['is_doctor'] = context.user_data['judge']['is_doctor']
    else:
        context.user_data['is_judge'] = False

    if participant.status_code == 200:
        context.user_data['is_participant'] = True
        context.user_data['participant'] = participant.json()

        # сохряняем в базу идентификатор участника
        participant_session = {
            'participant': context.user_data['participant']['id'],
            'chat_id': update.message.chat_id
        }

        Api.post('participant-sessions', participant_session)
    else:
        context.user_data['is_participant'] = False

    is_judge = context.user_data['is_judge']
    is_doctor = context.user_data['is_doctor']
    is_participant = context.user_data['is_participant']

    # выводим приветствие (или не выводим)
    if is_judge and is_doctor:
        judge = context.user_data['judge']

        reply_markdown = f'*Привет, {judge["first_name"]}!*\n' \
                         'Вы доктор конкурса.\n' \
                         f'{separator}\n' \
                         '*Команды:*\n' \
                         '/doctor - оценить участника'

        update.message.reply_markdown(reply_markdown)
    elif is_judge:
        judge = context.user_data['judge']

        reply_markdown = f'*Привет, {judge["first_name"]}!*\n' \
                         'Вы судья конкурса.\n' \
                         f'{separator}\n' \
                         '*Команды:*\n' \
                         '/rate - оценить участника'

        update.message.reply_markdown(reply_markdown)
    elif is_participant:
        participant = context.user_data['participant']

        reply_markdown = f'*Привет, {participant["first_name"]}!*\n' \
                         'Вы участник конкурса.\n' \
                         'От меня вы будете получать сообщения о своих оценках.\n'

        update.message.reply_markdown(reply_markdown)


startHandler = CommandHandler('start', start)
