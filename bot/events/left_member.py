from telegram.ext import MessageHandler, Filters
from ..config import BOT_USERNAME
from ..lib.common import db, clean
from tinydb import Query


def handle(update, ctx):
    # This method is inteded as a clean up
    # If the captcha has not been solved, the welcome message
    # still remains in the group and must be removed
    # If the captcha has not been solved, the database entry
    # still exists and must be removed

    # check if self and ignore
    if update.message.left_chat_member.username == BOT_USERNAME:
        return None

    return clean(update=update,
                 ctx=ctx)

    group_id = update.effective_chat.id
    user_id = update.message.left_chat_member.id

    print(ctx.user_data[group_id])

    User = Query()

    # Delete the welcome msg  when user leaves group
    # This is done in case captcha has not been
    # solved.
    result = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )
    if(len(result) == 0):
        return None

    try:
        update.message.bot.delete_message(
            chat_id=group_id,
            message_id=result[0]['message_id']
        )
    except Exception as e:
        # Maybe captcha was solved and the message was deleted already?
        print("Deleting initial message failed: ")
        print(str(e))

    # Attempt to delete the database entry
    try:
        db.remove(
            (User.group_id == group_id) & (User.user_id == user_id)
        )
    except Exception as e:
        print("Deleting database  record failed: ")
        print(str(e))


handler = MessageHandler(Filters.status_update.left_chat_member, handle)
