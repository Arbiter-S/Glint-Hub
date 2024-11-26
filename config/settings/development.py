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

