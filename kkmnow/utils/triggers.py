import os
from os import listdir
from os.path import isfile, join
import requests


def send_telegram(message) :
    params = {
        'chat_id': os.getenv("TELEGRAM_CHAT_ID"),
        'text': message
    }
    tf_url = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/sendMessage'
    r = requests.get(url=tf_url, data = params)