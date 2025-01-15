import random
import pytest
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from faker import Faker
from carts.models import Cart

User = get_user_model()
fake = Faker()


@pytest.fixture
def add_products_to_cart(client, create_products):
    user = User.objects.create_user(username='JohnDoe', password='StrongPassword123!', email='johndoe@example.com')
    Cart.objects.create(user=user)
    client.force_authenticate(user)
    selected_products = []
    for _ in range(5):
        product = random.choice(create_products)
        quantity = max(1, product.in_stock)
        selected_products.append([product, quantity])
        create_products.remove(product)
        body = {
                "product_id": product.id,
                "product_quantity": quantity,
            }
        response = client.post(reverse('CartRetrieve'), body, format='json')
        assert response.status_code == 201

    return selected_products, client

@pytest.mark.django_db
def test_cart_retrieve_success(add_products_to_cart):
    selected_products, auth_client = add_products_to_cart
    response = auth_client.get(reverse('CartRetrieve')).json()
    for i in range(len(selected_products)):
        assert response['items'][i]['product_quantity'] == selected_products[i][1]
        assert response['items'][i]['product']['id'] == selected_products[i][0].id
        assert response['items'][i]['product']['name'] == selected_products[i][0].name
        assert response['items'][i]['product']['description'] == selected_products[i][0].description
        assert float(response['items'][i]['product']['weight']) == float(selected_products[i][0].weight)
        assert response['items'][i]['product']['color'] == selected_products[i][0].color
        assert response['items'][i]['product']['in_stock'] == selected_products[i][0].in_stock
        assert response['items'][i]['product']['category'] == selected_products[i][0].category
