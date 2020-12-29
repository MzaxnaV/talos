from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ChatPermissions)
from telegram.utils.helpers import mention_markdown
from tinydb import TinyDB, Query
from ..config import RULES_URI, START_MSG
from loguru import logger
import requests
import json
import random
from .models import Captcha, orm

db = TinyDB('.userdata')
rules = json.loads(requests.get(RULES_URI).text)

mute_perms = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False
)

unmute_perms = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=False,
    can_send_other_messages=False
)

okay_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Okay', callback_data='self_destruct')]
])


def get_mention(user):
    name = user.username if user.username else user.id
    return mention_markdown(user_id=user.id, name=str(name), version=2)


# Check if a database entry  exists with the given
# Group id and user id
# For use with tinydb - will be removed
def user_exists(user_id, group_id):
    User = Query()
    user = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )
    return len(user)


# Check if a captcah exists with specified user id and group id
def captcha_exists(user_id, group_id):
    with orm.db_session:
        return orm.exists(u for u in Captcha if u.group_id == group_id
                          and user_id == user_id)


def get_captcha(group_id, user_id):
    question = random.choice(range(0, len(rules)))
    answer = question + 1
    choices = [answer]

    while len(choices) < 4:
        rand_choice = random.choice(range(1, len(rules)+1))
        if(rand_choice != question and rand_choice not in choices):
            choices.append(rand_choice)

    random.shuffle(choices)

    choices_kb = [
        [
            InlineKeyboardButton(text=choice,
                                 callback_data=(f'verify_captcha_{group_id}_'
                                                f'{choice}'))
        ]
        for choice in choices
    ]

    return {
        'question': START_MSG.format(question=rules[question]),
        'choices': InlineKeyboardMarkup(choices_kb),
        'valid_answer': answer
    }


# Clean method for use with tinydb - will  be removed
def clean(update, ctx, group_id=None):
    User = Query()
    if not group_id:
        group_id = update.effective_chat.id

    try:
        bot = update.callback_query.bot
    except AttributeError:
        bot = update.message.bot

    try:
        user_id = update.message.left_chat_member.id
    except AttributeError:
        user_id = update.effective_chat.id

    # Attempt to clear captcha object stored in user context data
    try:
        del ctx.user_data[group_id]
    except Exception:
        pass

    result = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )
    if not len(result) > 0:
        return False
    result = result[0]

    # Attempt to remove welcome message
    try:
        bot.delete_message(
            chat_id=group_id,
            message_id=result['message_id']
        )
    except Exception as e:
        logger.error(
            f'Could not delete initial message for {user_id}  due to {e}'
        )

    # Remove database entry
    try:
        db.remove(
            doc_ids=[result.doc_id]
        )
    except Exception as e:
        logger.error(f'Record {result.doc_id} could not be deleted : {e}')


# Clean method to work with sqlite
def clean_new(update, ctx, group_id=None):
    if not group_id:
        group_id = update.effective_chat.id

    try:
        bot = update.callback_query.bot
    except AttributeError:
        bot = update.message.bot

    try:
        user_id = update.message.left_chat_member.id
    except AttributeError:
        user_id = update.effective_chat.id

    # Attempt to clear captcha object stored in user context data
    try:
        del ctx.user_data[group_id]
    except Exception:
        pass

    with orm.db_session:
        result = Captcha.select(lambda c:  c.group_id == group_id and
                                user_id == user_id).first()
        if not result:
            return False
        print(result.user_id)

        # Attempt to remove welcome message
        try:
            bot.delete_message(
                chat_id=group_id,
                message_id=result.message_id
            )
        except Exception as e:
            logger.error(
                f'Could not delete initial message for {user_id}  due to {e}'
            )

        # Remove database entry
        try:
            result.delete()
        except Exception as e:
            logger.error(f'Record {result.doc_id} could not be deleted : {e}')
