import requests
from requests.exceptions import JSONDecodeError
import os
from dotenv import load_dotenv
from celery import shared_task
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)
load_dotenv()

@shared_task
def update_price():
    try:
        response = requests.get(f"http://api.navasan.tech/latest/?api_key={os.getenv('API_KEY')}&item=18ayar")
        response_json = response.json()
    except JSONDecodeError:
        logger.error(f"Unable to update price. status code: {response.status_code}")
        return
    price = int(response_json['18ayar']['value'])
    cache.set('price', price, None)