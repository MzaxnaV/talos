from telegram.ext import MessageHandler, Filters
from telegram import  InlineKeyboardMarkup, InlineKeyboardButton
from ..lib.common import get_captcha, db, mute_perms, get_mention, me
from tinydb import Query

def handle(update, ctx):
    # Ignore if self
    if update.message.new_chat_members[0].username == me:
        return None

    group_id = update.effective_chat.id
    user_id = update.message.new_chat_members[0].id

    captcha = get_captcha(group_id, user_id)

    update.message.bot.restrict_chat_member(
        chat_id=group_id,
        user_id=user_id,
        permissions=mute_perms
    )

    url = f't.me/rulescaptcha_bot?start={update.effective_chat.id}'
    rules_url = f't.me/pyindiarules'
    keyboard = [
        [
            InlineKeyboardButton(text='Click to unmute',url=url)
        ],
        [
            InlineKeyboardButton(text='Rules', url=rules_url)
        ]
    ]
    user_mention = get_mention(update.effective_user)
    text=(f'Hey there, {user_mention}. You\'ve been muted until you solve a'
          ' captcha.')
    msg = update.message.bot.send_message(
        chat_id=group_id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="MARKDOWN"
    )

    User = Query()
    db.upsert(
        {
            "group_id":group_id,
            "user_id":user_id,
            "solved":False,
            "valid_answer":None,
            "message_id": msg.message_id
        },
        (
            (User.group_id == group_id) & ( User.user_id == user_id )
        )
    )

handler = MessageHandler(Filters.status_update.new_chat_members, handle)
