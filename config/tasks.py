import requests
from requests.exceptions import JSONDecodeError
import os
from dotenv import load_dotenv
from django.core.cache import caches
from celery import shared_task

load_dotenv()

cache = caches['docker']

@shared_task
def update_price():
    try:
        response = requests.get(f"http://api.navasan.tech/latest/?api_key={os.getenv('API_KEY')}&item=18ayar").json()
    except JSONDecodeError:
        # TODO: Take some measures to alert the issue or prices not getting updated
        return
    price = int(response['18ayar']['value'])
    cache.set('price', price, None)