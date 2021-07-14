from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import csv


@shared_task
def stocksBot(stock_name, group_name: str):
    url = "https://stooq.com/q/l/?s=" + stock_name + "&f=sd2t2ohlcv&h&e=csv"
    quote = get_data_from_url(url)
    print(quote)
    body_message = f"{stock_name} quote is $ {quote} + per share"
    bot_message = {
        "username": "bot",
        "message": body_message
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'message_from_task',
            'message': bot_message,
            "action": "new_message",
        })
    return bot_message


def get_data_from_url(url: str) -> str:
    """Download the csv, extract and parse then return the needed info"""
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        csv_content = csv.reader(decoded_content.splitlines(), delimiter=',')
        list_content = list(csv_content)
        index_close = list_content[0].index('Close')
        quote_value = list_content[1][index_close]
        return quote_value
