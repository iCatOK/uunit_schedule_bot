import os

from peewee import *
from telebot import TeleBot

db = SqliteDatabase(u"%s\main.db" % os.getcwd())
default_items_per_page = 15


def init_db(models):
    # db.drop_tables(models)
    db.create_tables(models)


def peewee_sql(func):
    def _wrapper(*args, **kwargs):
        with db.atomic() as transaction:
            try:
                result = func(*args, **kwargs)
                return result
            except DatabaseError as e:
                transaction.rollback()
                return e
    return _wrapper


bot_token = os.environ.get("UUNIT_BOT_TOKEN")

bot = TeleBot(bot_token)

# scheduler = Scheduler(tzinfo=timezone.utc, n_threads=0)
# daily_time = datetime(year=2022, month=12, day=28, hour=3, minute=33, tzinfo=timezone.utc)
