import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "django_filters",
    "rest_framework",
    "drf_spectacular",
    # apps
    "users",
    "products",
    "carts",
    "orders",
    "transactions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# logging configuration
# TODO: logging in general have still so much room for improvement
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format": "[{asctime}] {levelname} {message} {name}",
            "datefmt": "%d/%b/%Y:%H:%M:%S %z",
            "style": "{",
        },
        "simple_gunicorn": {
            "format": "{levelname} {message} {name}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "django_general": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/django_general.log",
            "formatter": "simple",
        },
        "root_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/root.log",
            "formatter": "simple",
        },
        # gunicorn related handlers
        "console_gunicorn": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple_gunicorn",
        },
        "gunicorn_access": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/gunicorn_access.log",
        },
        "gunicorn_error": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/gunicorn_error.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_general", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.access": {
            "handlers": ["gunicorn_access", "console_gunicorn"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["gunicorn_error", "console_gunicorn"],
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["root_file", "console"],
        "level": "INFO",
    },
}


AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["users.authentication.EmailBackend"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# TODO: spectacular has too much boiler plate code with many warnings even if you schema is accurate. Try to solve them.


SPECTACULAR_SETTINGS = {
    "TITLE": "GlintHub",
    "DESCRIPTION": "GlintHub is an API to manage an online shop selling gold related products",
    "VERSION": "0.9.0",
    "AUTHENTICATION_WHITELIST": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# Celery configuration
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_BEAT_SCHEDULE = {
    "update_price": {"task": "config.tasks.update_price", "schedule": 60 * 30}
}
