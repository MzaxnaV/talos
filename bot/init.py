import os
from dotenv import load_dotenv
load_dotenv()
from telegram.ext import Updater
from .lib import common
from .events import new_member, start, verify_captcha, left_member

token = os.getenv('BOT_TOKEN')

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(new_member.handler)
dispatcher.add_handler(start.handler)
dispatcher.add_handler(verify_captcha.handler)
dispatcher.add_handler(left_member.handler)

updater.start_polling()
updater.idle()
