from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-horu%2^i!qty2t+y2vf6fhk$6*t4%6z-23qgx1p_jgevbm^df4'

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'TEST' : {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_sqlite3',
    }
}

#TODO: Should I optimize containers and installed apps based on their responsibility or should I keep them consistent?
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]
