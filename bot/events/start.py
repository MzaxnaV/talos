from telegram.ext import CommandHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ..lib.common import db, user_exists
from tinydb import Query


# def resolve(update, ctx):
    # try:
        # group_id = int(update.message.text.split(' ')[1])
    # except Exception:
        # update.message.reply_text("I'm just a captcha bot")
        # return None
    # user_id = update.effective_user.id

    # User = Query()
    # user = db.search(
        # (User.group_id == group_id) & (User.user_id == user_id)
    # )
    # if not len(user):
        # update.message.reply_text(("You do not have any captcha to solve"
                                  # " right now in this group"))
        # return None

    # captcha = get_captcha(group_id, user_id)
    # db.update(
        # {'valid_answer': captcha['valid_answer']},
        # (
            # (User.group_id == group_id) & (User.user_id == user_id)
        # )
    # )
    # update.message.bot.send_message(
        # chat_id=user_id,
        # text=captcha['question'],
        # reply_markup=captcha['choices'],
        # parse_mode="MARKDOWN"
    # )

def resolve(update, ctx):
    user_id = update.effective_user.id
    try:
        group_id = int(update.message.text.split(' ')[1])
    except IndexError:
        update.message.reply_text('I\'m just a captcha bot')
        return None


    # if not user_exists(user_id=user_id, group_id=group_id):
        # return update.message.reply_text(
            # 'You do not have any captcha to solve in this group right now')

    cb_data = f'verify_captcha_{group_id}'
    update.message.bot.send_message(
        chat_id=user_id,
        text='Click Start to begin captcha',
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text='Start',
                                      callback_data=cb_data)]
            ]
        ),
        parse_mode='MARKDOWN'
    )


handler = CommandHandler(command='start',
                         callback=resolve,
                         filters=Filters.private)
