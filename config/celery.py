import os
from celery import Celery
from celery.signals import setup_logging
from utils.generic import fetch_settings

settings_path = fetch_settings()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{settings_path}")

celery = Celery("config")

celery.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from django.conf import settings
    from logging.config import dictConfig

    dictConfig(settings.LOGGING)


celery.autodiscover_tasks(["config"])
