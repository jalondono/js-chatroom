from celery import Celery
from nose.tools import eq_

from chat import tasks


def test_task_running():
    result = add.apply(args=(4, 4)).get()
    eq_(result, 8)


def test_user_bot_response():
    # Verify that the message belong to the bot
    result = tasks.stocksBot.apply(args=('aapl.us', 'room')).get()
    eq_(result["username"], "bot")


def test_len_bot_message():
    # Verify that the message isn't empty
    result = tasks.stocksBot.apply(args=('aapl.us', 'room')).get()
    valid_len = len(result["message"]) > 0
    eq_(valid_len, True)


def test_is_message_str():
    # verify if the massage result in an string
    result = tasks.stocksBot.apply(args=('aapl.us', 'room')).get()
    str_instance = isinstance(result["message"], str)
    eq_(str_instance, True)


celery = Celery()


# django nose example
@celery.task
def add(x, y):
    return x + y
