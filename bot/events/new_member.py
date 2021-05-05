from ..config import BOT_USERNAME, RULES_URI_HUMAN, ENABLE_WELCOME_MSG
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from ..lib.common import db, mute_perms, get_mention
from loguru import logger
from tinydb import Query
from ..lib.models import Captcha, orm


def handle(update, ctx):
    # Ignore if self
    if update.message.new_chat_members[0].username == BOT_USERNAME:
        logger.info(f"Talos has been added to {update.effective_chat.id}")
        return None

    group_id = update.effective_chat.id
    user_id = update.message.new_chat_members[0].id
    msgid = None

    try:
        update.message.bot.restrict_chat_member(
            chat_id=group_id,
            user_id=user_id,
            permissions=mute_perms
        )
    except Exception as e:
        logger.error(
            (f'Muting user {update.effective_user.id} on Group {group_id}'
             f' failed  due to {e}')
        )
        return False

    if ENABLE_WELCOME_MSG:
        url = f't.me/{BOT_USERNAME}?start={update.effective_chat.id}'
        keyboard = [
            [
                InlineKeyboardButton(text='Click to unmute', url=url)
            ],
            [
                InlineKeyboardButton(text='Rules', url=RULES_URI_HUMAN)
            ]
        ]
        user_mention = get_mention(update.effective_user)
        text = (f'Hey there, {user_mention}. You\'ve been muted until you '
                'solve a captcha.')
        msg = update.message.bot.send_message(
            chat_id=group_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="MARKDOWN"
        )
        msgid = msg.message_id

    User = Query()
    db.upsert(
        {
            "group_id": group_id,
            "user_id": user_id,
            "message_id": msgid
        },
        (
            (User.group_id == group_id) & (User.user_id == user_id)
        )
    )
    with orm.db_session:
        Captcha(user_id=user_id, group_id=str(group_id), message_id=str(msgid))
        orm.commit()


handler = MessageHandler(Filters.status_update.new_chat_members, handle)
