from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ChatPermissions)
from telegram.utils.helpers import mention_markdown
from tinydb import TinyDB, Query
from ..config import RULES_URI, START_MSG
import requests
import json
import random


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
def user_exists(user_id, group_id):
    User = Query()
    user = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )
    return len(user)


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


def clean(update, ctx, group_id=None):
    User = Query()
    if not group_id:
        group_id = update.effective_chat.id

    try:
        bot = update.callback_query.bot
    except AttributeError:
        bot = update.message.bot

    try:
        user_id = update.left_chat_member.id
    except AttributeError:
        user_id = update.effective_chat.id

    # Attempt to remove welcome message
    try:
        result = db.search(
            (User.group_id == group_id) & (User.user_id == user_id)
        )[0]
        bot.delete_message(
            chat_id=group_id,
            message_id=result['message_id']
        )
    except Exception as e:
        print(str(e))

    try:
        del ctx.user_data[group_id]
    except Exception as e:
        print(str(e))

    # Remove database entry
    try:
        db.remove(
            doc_ids=[result.doc_id]
        )
    except Exception as e:
        print(str(e))
