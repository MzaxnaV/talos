import os
from dotenv import load_dotenv
load_dotenv()
from telegram.ext import Updater
from .lib import common
from .events import new_member, start, verify_captcha

token = os.getenv('BOT_TOKEN')
rules_uri = os.getenv('RULES_URI')


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(new_member.handler)
dispatcher.add_handler(start.handler)
dispatcher.add_handler(verify_captcha.handler)

updater.start_polling()
updater.idle()
