from telegram.ext import CommandHandler
from ..config import BOT_MASTER
from loguru import logger


def resolve(update, ctx):
    if update.effective_user.id != BOT_MASTER:
        return False
    userid = update.message.text.split(' ')[1]
    try:
        update.message.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=userid
        )
    except Exception as e:
        logger.error(
            (f'Unbanning user {userid} from group {update.effective_chat.id}'
             f' failed due to {e}')
        )
    update.message.reply_text(f'{userid} has been unbanned')


handler = CommandHandler('unban', resolve)
