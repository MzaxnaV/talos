from telegram.ext import CommandHandler
from ..config import BOT_MASTER


def resolve(update, ctx):
    if update.effective_user.id != BOT_MASTER:
        return False
    userid = update.message.text.split(' ')[1]
    update.message.bot.unban_chat_member(
        chat_id=update.effective_chat.id,
        user_id=userid
    )
    update.message.reply_text(f'{userid} has been unbanned')


handler = CommandHandler('unban', resolve)
