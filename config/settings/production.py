from .base import *
from os import getenv
from dotenv import load_dotenv

load_dotenv()


DEBUG = False

ALLOWED_HOSTS = ['*'] # nginx handles host header attacks but better change it to make sure

SECRET_KEY = getenv('SECRET_KEY')

# Removing DRF browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].remove('rest_framework.renderers.BrowsableAPIRenderer')
