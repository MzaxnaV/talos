from .config import BOT_TOKEN
from telegram.ext import Updater, JobQueue

updater = Updater(BOT_TOKEN, use_context=True)
jobq = JobQueue()
