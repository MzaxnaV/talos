from telegram.ext import CommandHandler


def resolve(update, ctx):
    userid = update.message.text.split(' ')[1]
    update.message.bot.unban_chat_member(
        chat_id=update.effective_chat.id,
        user_id=userid
    )
    update.message.reply_text(f'{userid} has been unbanned')


handler = CommandHandler('unban', resolve)
