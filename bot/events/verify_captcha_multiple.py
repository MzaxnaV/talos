from ..config import QUESTION_QUANTITY
from telegram.ext import CallbackQueryHandler
from ..lib.common import unmute_perms, db, user_exists
from ..lib.captcha import Captcha, WrongAnswerError
from tinydb import Query


def resolve(update, ctx):
    callback_data = update.callback_query.data.split('_')
    group_id = int(callback_data[2])
    user_id = update.effective_user.id

    # Validate that this should happen
    group_id = 123
    # if not user_exists(user_id=user_id,
                       # group_id=group_id):
        # return update.callback_query.answer('Oops! Invalid action')
    # Check if a captcha has been set
    try:
        captcha = ctx.user_data[group_id]
    except KeyError:
        # Captcha not set - set it now
        captcha = ctx.user_data[group_id] = Captcha(
            total_iterations=QUESTION_QUANTITY,
            errors_allowed=3,
            group_id=group_id
            # callback_data[2]
        )

    # Check if an answer is involved in the callback data
    try:
        answer = callback_data[3]
        # If answer is valid retrieve next question
        # and increment solved counter
        captcha == answer
        captcha + 1
    except WrongAnswerError:
        # wrong answer
        captcha - 1
        if captcha.has_failed():
            kick(update, captcha.group_id)
            clean(update, captcha.group_id)
            update.callback_query.answer(
                'You have failed the captcha. You will now be kicked.'
            )
            return update.callback_query.message.delete()
        else:
            return update.callback_query.answer('WRONG')
    except IndexError:
        # No answer
        pass

    # Self explanatory - unmute the user
    if captcha.is_solved():
        unmute(update, captcha.group_id)
        clean(update=update, group_id=captcha.group_id)
        return

    try:
        update.callback_query.edit_message_text(
            text=str(captcha),
            reply_markup=captcha.answer_choices()
        )
    except Exception as e:
        print(str(e))
        pass


def kick(update, group_id):
    # Kick user
    try:
        update.callback_query.bot.kick_chat_member(
            chat_id=group_id,
            user_id=update.effective_user.id
         )
    except Exception as e:
        print(str(e))

    return None


def unmute(update, group_id):
    try:
        update.callback_query.bot.restrict_chat_member(
            chat_id=group_id,
            user_id=update.effective_user.id,
            permissions=unmute_perms
        )
    except Exception as e:
        print(str(e))

    return None


# attempt to delete  the welcome message
# and clean database entry
def clean(update, group_id):
    User = Query()
    user_id = update.effective_chat.id
    result = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )


handler = CallbackQueryHandler(
    callback=resolve,
    pattern='^verify_captcha_')
