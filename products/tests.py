from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from products.models import Product
from faker import Faker
import random
from products.views import ProductViewSet

fake = Faker()

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
            in_stock=random.randint(0, 100),
            category=random.choice(categories),
            purity=18,
            picture=None,
        )
        products.append(product)

    return products


def test_products_method_not_allowed():
    client = APIClient()
    response = client.post(reverse('Product-list'))
    assert response.status_code == 405
    response = client.put(reverse('Product-list'))
    assert response.status_code == 405
    response = client.patch(reverse('Product-list'))
    assert response.status_code == 405
    response = client.delete(reverse('Product-list'))
    assert response.status_code == 405


@pytest.mark.django_db
def test_products_list_successful(create_products):
    client = APIClient()
    response = client.get(reverse('Product-list'), format='json')
    assert response.status_code == 200
    assert response.json()['count'] == Product.objects.all().count()

@pytest.mark.django_db
def test_products_list_pagination(create_products):
    client = APIClient()
    response = client.get(reverse('Product-list'), format='json')
    assert len(response.json()['results']) == ProductViewSet.ProductPagination.page_size

@pytest.mark.parametrize('ordering', ['price', 'created_at', '-price', '-created_at'])
@pytest.mark.django_db
def test_products_list_ordering(create_products, ordering):
    client = APIClient()
    response = client.get(reverse('Product-list') + f'?ordering={ordering}', format='json')
    assert response.status_code == 200

    if ordering[0] == '-':
        reverse_flag = True
        ordering = ordering[1:]
    else:
        reverse_flag = False
    products = response.json()['results']
    ordered = [product[ordering] for product in products]

    assert ordered == sorted(ordered, reverse=reverse_flag)


@pytest.mark.django_db
def test_products_retrieve_successful(create_products):
    client = APIClient()
    for _ in range(3):
        product = random.choice(create_products)
        response = client.get(reverse('Product-detail', kwargs={'pk': product.pk}), format='json')
        assert response.status_code == 200
        response_data = response.json()

        assert product.name == response_data['name']
        assert product.color == response_data['color']
        assert product.id == response_data['id']
        assert product.description == response_data['description']
        assert float(product.weight) == float(response_data['weight'])
        assert product.in_stock == response_data['in_stock']
        assert product.category == response_data['category']
        assert product.purity == response_data['purity']
        assert product.picture == response_data['picture']


@pytest.mark.django_db
def test_products_not_found(create_products):
    client = APIClient()
    response = client.get(reverse('Product-detail', kwargs={'pk': 51}), format='json')
    assert response.status_code == 404
    assert response.json() == {"detail": "No Product matches the given query."}
