from telegram.ext import CommandHandler
from .api import Api


def start(update, context):
    if 'is_judge' not in context.user_data:
        judges = Api.get('judges')
        judge_usernames = [judge['telegram_username'] for judge in judges]
        username = update.message.from_user.username
        context.user_data['is_judge'] = username in judge_usernames

    is_judge = context.user_data['is_judge']

    if is_judge:
        judge = Api.get('judges/{}'.format(update.message.from_user.username))
        context.user_data['judge'] = judge

    reply_markdown = '*Привет, {}!*\n' \
                     '----------\n' \
                     '*Команды:*\n' \
                     .format(update.message.from_user.first_name)

    if is_judge:
        reply_markdown += '/rate - оценить участника'

    update.message.reply_markdown(reply_markdown)


startHandler = CommandHandler('start', start)
