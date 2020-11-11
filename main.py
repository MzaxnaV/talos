from bot.dispatcher import updater, jobq

updater.start_polling()
jobq.start()
updater.idle()
