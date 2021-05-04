from telegram.ext import CallbackQueryHandler
from ..lib.common import unmute_perms, clean_new, captcha_exists
from ..lib.captcha import Captcha, WrongAnswerError
from ..config import (QUESTION_QUANTITY, ERRORS_ALLOWED, TZ,
                      BAN_PERIOD)
from datetime import datetime, timedelta
from loguru import logger


def resolve(update, ctx):
    callback_data = update.callback_query.data.split('_')
    group_id = int(callback_data[2])
    user_id = update.effective_user.id

    # Validate that this should happen
    if not captcha_exists(user_id=user_id,
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
        clean_new(update=update, ctx=ctx,
              group_id=captcha.group_id)
        return update.callback_query.message.delete()

    try:
        update.callback_query.edit_message_text(
            text=str(captcha),
            reply_markup=captcha.answer_choices(),
            parse_mode="MARKDOWN"
        )
    except Exception as e:
        print(str(e))
        pass


def kick(update, group_id):
    # Kick user
    if BAN_PERIOD:
        unban_date = datetime.now(tz=TZ) + timedelta(minutes=2)
    else:
        unban_date = 0
    try:
        update.callback_query.bot.kick_chat_member(
            chat_id=group_id,
            user_id=update.effective_user.id,
            until_date=unban_date
         )
    except Exception as e:
        logger.error(
            (f'Kicking user {update.effective_user.id} from Group {group_id}'
             f' failed  due to {e}')
        )
    return None


def unmute(update, group_id):
    try:
        update.callback_query.bot.restrict_chat_member(
            chat_id=group_id,
            user_id=update.effective_user.id,
            permissions=unmute_perms
        )
    except Exception as e:
        logger.error(
            (f'Unmuting user {update.effective_user.id} on Group {group_id}'
             f' failed  due to {e}')
        )

    return None


handler = CallbackQueryHandler(
    callback=resolve,
    pattern='^verify_captcha_')
