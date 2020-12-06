from .events import (new_member, start, left_member,
                     verify_captcha_multiple, unban)
from .init import updater, jobq

dispatcher = updater.dispatcher
jobq.set_dispatcher(dispatcher)

dispatcher.add_handler(new_member.handler)
dispatcher.add_handler(start.handler)
dispatcher.add_handler(unban.handler)
dispatcher.add_handler(left_member.handler)
dispatcher.add_handler(verify_captcha_multiple.handler)
