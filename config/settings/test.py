# The sole purpose for this file is have a SQLite db for tests while having a dockerized postgres db for everything else
# TODO: See if there is a cleaner way to handle this file without the need for an additional file. So far I have tried
# changing it dynamically with a pytest fixture and setting a TEST db. pytest-django plugin has no flexibility on this issue
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_sqlite3',
    },
}