from ..config import QUESTION_QUANTITY
from telegram.ext import CommandHandler, CallbackQueryHandler
from ..lib.common import db
from ..lib.question import Question
from tinydb import Query


def resolve(update, ctx):
    print(QUESTION_QUANTITY)
    print(Query)
    print(db)
    print(Question)


handler = CallbackQueryHandler(
    callback=resolve,
    pattern='verify_captcha_')

test_handler = CommandHandler('test', resolve)
