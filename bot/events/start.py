from telegram.ext import CommandHandler, Filters
from ..lib.common import db, get_captcha
from tinydb import Query


def resolve(update, ctx):
    try:
        group_id = int(update.message.text.split(' ')[1])
    except Exception:
        update.message.reply_text("I'm just a captcha bot")
        return None
    user_id = update.effective_user.id

    User = Query()
    user = db.search(
        (User.group_id == group_id) & (User.user_id == user_id)
    )
    if not len(user):
        update.message.reply_text(("You do not have any capthas to solve"
                                  " right now in this group"))
        return None

    captcha = get_captcha(group_id, user_id)
    db.update(
        {'valid_answer': captcha['valid_answer']},
        (
            (User.group_id == group_id) & (User.user_id == user_id)
        )
    )
    update.message.bot.send_message(
        chat_id=user_id,
        text=captcha['question'],
        reply_markup=captcha['choices'],
        parse_mode="MARKDOWN"
    )


handler = CommandHandler(command='start',
                         callback=resolve,
                         filters=Filters.private)
