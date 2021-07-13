from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import csv
import json


@shared_task
def stocksBot(stock_name, group_name: str):
    bot_result = {}
    return bot_result
