from django.core.cache import cache
from django.db.models import F
from redis import ConnectionError
from logging import getLogger
from products.models import Product

logger = getLogger(__name__)

def fetch_price():
    try:
        price = cache.get('price', 3500000)
    # redis instance is not accessible
    except ConnectionError:
        logger.error(f'Could not fetch price from redis')
        price = 3500000
    return price


def add_price_field(queryset=None):
    """
    Adds a new field 'price' to the queryset containing Product instances.
    If queryset is not given it will return all instances of Product with the additional field.

    Args:
        queryset: Queryset containing Product instances

    Returns: Queryset containing Product instances with an additional field named "price"

    """
    price_per_gram = fetch_price()

    if queryset:
        qs = queryset.annotate(price=F('weight') * price_per_gram)

    else:
        qs = Product.objects.annotate(price=F('weight') * price_per_gram)
    return qs
    # TODO: Make price field an integer
