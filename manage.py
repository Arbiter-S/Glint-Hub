#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from utils.generic import fetch_settings
from dotenv import load_dotenv

load_dotenv(dotenv_path="Docker/.env")

# Making logs directory to avoid errors by the loggers
script_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(script_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)


settings = fetch_settings()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{settings}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
