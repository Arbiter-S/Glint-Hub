from secrets import randbelow
from django.core.cache import cache

def generate_code():
    """
    Generates a random 6-digit code
    """
    code = randbelow(900000) + 100000
    return code

def cache_email_code(user_id, verification_code):
    """
    Caches the verification code for a user for the next 5 minutes

    Args:
        user_id: Unique identifier for the user
        verification_code: Code to be cached

    Returns: None

    """

    cache.set(f'verify_email_{user_id}', verification_code, 60 * 5)