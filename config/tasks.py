import requests
import os
from dotenv import load_dotenv
from django.core.cache import cache
from random import randint
from celery import shared_task
load_dotenv()

@shared_task
def update_price():
    response = requests.get(f"http://api.navasan.tech/latest/?api_key={os.getenv('API_KEY')}&item=18ayar").json()
    price = int(response['18ayar']['value'])
    cache.set('price', price, 60 * 120)