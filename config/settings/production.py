import os
from .base import *
from os import getenv
from dotenv import load_dotenv

load_dotenv()


DEBUG = False

ALLOWED_HOSTS = ['*'] # nginx handles host header attacks but better change it to make sure

SECRET_KEY = getenv('SECRET_KEY')

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'pgdb',
        'PORT': '5432',
    },
}
