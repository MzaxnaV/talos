from pony import orm
import os

db = orm.Database()


class User(db.Entity):
    _table_ = "users"
    user_id = orm.Required(int)
    warns = orm.Optional(int)
    groups = orm.Optional(orm.Json)
    warn_log = orm.Optional(orm.StrArray)
    ban_log = orm.Optional(orm.StrArray)


class Captcha(db.Entity):
    _table_ = "captchas"
    user_id = orm.Required(int)
    group_id = orm.Required(str)
    message_id = orm.Optional(str)


db.bind(provider='sqlite',
        filename=f'{os.getenv("PWD")}/.db',
        create_db=True)
db.generate_mapping(create_tables=True)
