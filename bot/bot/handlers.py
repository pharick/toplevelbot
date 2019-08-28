from types import SimpleNamespace
from telegram.ext import CommandHandler
from .api import fetch_api


def start(update, context):
    if 'is_judge' not in context.user_data:
        judges = fetch_api('judges')
        judge_usernames = [judge['telegram_username'] for judge in judges]
        username = update.message.from_user.username
        context.user_data['is_judge'] = username in judge_usernames

    is_judge = context.user_data['is_judge']

    reply_text = 'Привет, {}.\n'.format(update.message.from_user.first_name)

    if is_judge:
        reply_text += 'Вы можете оценивать участников.'

    update.message.reply_text(reply_text)


startHandler = CommandHandler('start', start)
