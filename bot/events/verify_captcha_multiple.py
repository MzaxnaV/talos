from ..config import QUESTION_QUANTITY, ERRORS_ALLOWED
from telegram.ext import CallbackQueryHandler
from ..lib.common import unmute_perms, user_exists, clean
from ..lib.captcha import Captcha, WrongAnswerError


def resolve(update, ctx):
    callback_data = update.callback_query.data.split('_')
    group_id = int(callback_data[2])
    user_id = update.effective_user.id

    # Validate that this should happen
    if not user_exists(user_id=user_id,
                       group_id=group_id):
        return update.callback_query.answer('Oops! Invalid action')
    # Check if a captcha has been set
    try:
        captcha = ctx.user_data[group_id]
    except KeyError:
        captcha = ctx.user_data[group_id] = Captcha(
            total_iterations=QUESTION_QUANTITY,
            errors_allowed=ERRORS_ALLOWED,
            group_id=group_id
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
        # If user has failed multiple attepts - kick
        if captcha.has_failed():
            kick(update, captcha.group_id)
            update.callback_query.answer(
                "You've been kicked due to multiple incorrect answers."
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
        update.callback_query.answer("Congrats! You've been unmuted!")
        clean(update=update, ctx=ctx,
              group_id=captcha.group_id)
        return update.callback_query.message.delete()

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


handler = CallbackQueryHandler(
    callback=resolve,
    pattern='^verify_captcha_')
