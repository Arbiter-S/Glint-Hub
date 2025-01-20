import requests
from requests.exceptions import JSONDecodeError
import os
from celery import shared_task
import logging
from django.core.cache import caches
from django.conf import settings

cache_string = 'from_container' if 'from_container' in settings.CACHES else 'default'

cache = caches[cache_string]

logger = logging.getLogger(__name__)


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