from .events import new_member, start, verify_captcha, left_member
from .events import verify_captcha_multiple
from .init import updater, jobq

dispatcher = updater.dispatcher
jobq.set_dispatcher(dispatcher)

dispatcher.add_handler(new_member.handler)
dispatcher.add_handler(start.handler)
dispatcher.add_handler(verify_captcha.handler)
dispatcher.add_handler(left_member.handler)
dispatcher.add_handler(verify_captcha_multiple.test_handler)
