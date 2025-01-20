"""
WSGI config for GoldShop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from utils.generic import fetch_settings
from dotenv import load_dotenv

load_dotenv(dotenv_path="Docker/.env")

settings = fetch_settings()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{settings}')

application = get_wsgi_application()
