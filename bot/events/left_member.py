from telegram.ext import MessageHandler, Filters
from ..config import BOT_USERNAME
from ..lib.common import clean, clean_new
from loguru import logger


def handle(update, ctx):
    # This method is inteded as a clean up
    # If the captcha has not been solved, the welcome message
    # still remains in the group and must be removed
    # If the captcha has not been solved, the database entry
    # still exists and must be removed

    # check if self and ignore
    if update.message.left_chat_member.username == BOT_USERNAME:
        logger.info(
            f'Talos has been removed from group {update.effective_chat.id}'
        )
        return None

    return clean_new(update=update,
                     ctx=ctx)


handler = MessageHandler(Filters.status_update.left_chat_member, handle)
