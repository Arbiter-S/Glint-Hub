from django.core.cache import cache
from orders.models import Order
from utils.product import add_price_field


def get_order_price(order_instance: Order) -> int:
    """
    Utility function to  get the latest price for a given order instance

    Args:
        order_instance: Order instance to get the price for

    Returns: Current price for the order instance

    """
    products = add_price_field(order_instance.products.all())
    order_products = order_instance.orderproduct_set.all()

    total_price = 0
    for order_product in order_products:
        product_id = order_product.product.id
        product = products.get(pk=product_id)
        quantity = order_product.product_quantity
        price = product.price * quantity
        total_price += price

    return total_price
