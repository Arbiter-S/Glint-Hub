import pytest
from products.models import Product
import faker
import random
from rest_framework.test import APIClient

fake = faker.Faker()


@pytest.fixture()
def create_products():
    """
    A fixture which makes 50 dummy instances

    Returns: A list containing the dummy products
    """
    categories = ["necklace", "bracelet", "watch", "earring"]

    products = []

    for _ in range(50):
        product = Product.objects.create(
            name=fake.word().capitalize(),
            description=fake.text(max_nb_chars=200),
            weight=round(random.uniform(0.1, 99.99), 2),
            color=fake.color_name(),
            in_stock=random.randint(1, 100),
            category=random.choice(categories),
            purity=18,
            picture=None,
        )
        products.append(product)

    return products

@pytest.fixture()
def client():
    return APIClient()