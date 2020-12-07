from loguru import logger
from bot.dispatcher import updater, jobq

logger.add(
    "logs/{time}.log",
    rotation='00:00')
updater.start_polling()
jobq.start()
logger.info("Talos is now running")
updater.idle()
