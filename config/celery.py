import os
from celery import Celery
from utils.generic import fetch_settings
from celery.signals import setup_logging

settings_path = fetch_settings()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{settings_path}')

celery = Celery('config')

celery.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    from django.conf import settings

    dictConfig(settings.LOGGING)

celery.autodiscover_tasks(['config'])
