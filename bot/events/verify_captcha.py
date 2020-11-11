from telegram.ext import CallbackQueryHandler
from ..lib.common import db, get_captcha, unmute_perms, okay_keyboard
from tinydb import Query


def resolve(update, ctx):
    try:
        group_id = int(update.callback_query.data.split('_')[2])
        answer = int(update.callback_query.data.split('_')[3])
    except Exception:
        # invalid group id?
        return None

    user_id = update.effective_user.id
    User = Query()

    result = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )

    # User is either not part of group or
    # User has not pm'd the bot for captcha yet

    if not result:
        update.callback_query.edit_message_text(
            text='Oops, looks like you left the group',
            reply_markup=okay_keyboard
        )
        return None

    # Wrong answer
    if answer != result[0]['valid_answer']:
        captcha = get_captcha(group_id, user_id)

        # Update database with new captcha answer
        db.update(
            {"valid_answer": captcha['valid_answer']},
            (
                (User.group_id == group_id) & (User.user_id == user_id)
            )
        )

        # Update the message with new captcha and choices
        update.callback_query.edit_message_text(
            text=f"*WRONG ANSWER!*\n\n{captcha['question']}",
            reply_markup=captcha['choices'],
            parse_mode="MARKDOWN"
        )
        return None

    # Valid answer - unmute
    update.callback_query.bot.restrict_chat_member(
        chat_id=group_id,
        user_id=user_id,
        permissions=unmute_perms
    )

    # Now inform the cunt
    update.callback_query.edit_message_text(
        text="Captcha verified. You have been unmuted.",
        reply_markup=okay_keyboard
    )

    try:
        # Delete initial message in group
        update.callback_query.bot.delete_message(
            chat_id=group_id,
            message_id=result[0]['message_id']
        )
    except Exception as e:
        print("deleting initial message after verify failed: ")
        print(str(e))

    # Delete the database entry
    try:
        db.remove(
            (User.group_id == group_id) & (User.user_id == user_id)
        )
    except Exception as e:
        print("deleting  database entry after verify failed:")
        print(str(e))


handler = CallbackQueryHandler(callback=resolve,
                               pattern='verify_captcha_')
