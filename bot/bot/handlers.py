from telegram.ext import CommandHandler
from .api import Api
from .settings import separator


def start(update, context):
    username = update.message.from_user.username
    judge = Api.get(f'judges/{username}')

    if judge.status_code == 200:
        context.user_data['is_judge'] = True
        context.user_data['judge'] = judge.json()

    is_judge = context.user_data['is_judge']
    first_name = update.message.from_user.first_name

    reply_markdown = f'*Привет, {first_name}!*\n' \
                     f'{separator}\n' \
                     '*Команды:*\n'

    if is_judge:
        reply_markdown += '/rate - оценить участника'

    update.message.reply_markdown(reply_markdown)


startHandler = CommandHandler('start', start)
