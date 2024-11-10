import os
from celery import Celery
from utils.generic import fetch_settings

settings = fetch_settings()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{settings}')

celery = Celery('config')

celery.config_from_object('django.conf:settings', namespace='CELERY')

celery.autodiscover_tasks(['config'])
