from dotenv import load_dotenv
import os

load_dotenv()


def fetch_settings():
    settings = {
        "PRO": "production",
        "DEV": "development",
    }

    environment = settings.get(os.getenv("SETTINGS"), "development")
    return environment