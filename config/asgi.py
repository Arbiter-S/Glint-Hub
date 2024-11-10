"""
ASGI config for GoldShop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from utils.generic import fetch_settings

settings = fetch_settings()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{settings}')

application = get_asgi_application()
