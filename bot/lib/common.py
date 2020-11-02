from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ChatPermissions)
from telegram.utils.helpers import mention_markdown
from tinydb import TinyDB
import os
import requests
import json
import random
import re

db = TinyDB('.userdata')
me = os.getenv('BOT_USERNAME')
rules_uri = os.getenv('RULES_URI')
rules = json.loads(requests.get(rules_uri).text)
qstn = ('Hello there,\nYou have been muted.\nTo ensure smooth interaction'
        ' in this community, you are required to read the rules and solve'
        ' this captcha in order to verify that you have done the  same.\n'
        'At which number is the following rule listed in @pyindiarules\n'
        '\n*{question}*')

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
    [ InlineKeyboardButton(text='Okay', callback_data='foo') ]
])


def get_mention(user):
    name = user.username if user.username else user.id
    return mention_markdown(user_id=user.id, name=str(name), version=2)

def get_captcha(group_id, user_id):
    question = random.choice(range(0,len(rules)))
    answer = question + 1
    choices = [answer]

    while len(choices) < 4:
        rand_choice = random.choice(range(1, len(rules)+1))
        if(rand_choice != question and rand_choice not in choices):
            choices.append(rand_choice)

    random.shuffle(choices)

    choices_kb =[
        [
            InlineKeyboardButton(text=choice,
                                 callback_data=f'verify_captcha_{group_id}_{choice}')
        ]
        for choice in choices
    ]

    return {
        'question' : qstn.format(question=rules[question]),
        'choices': InlineKeyboardMarkup(choices_kb),
        'valid_answer': answer
    }
