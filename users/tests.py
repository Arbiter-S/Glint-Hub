import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


@pytest.mark.parametrize('password', ['asdfghjk', 'prj8', 951983354])
@pytest.mark.django_db
def test_register_with_weak_password(password):
    client = APIClient()
    body = {
        'username': 'SomeRandomName',
        'password': password,
        'email': 'testtest@gmail.com',
    }
    errors = {
        'asdfghjk': 'This password is too common.',
        'prj8': 'This password is too short. It must contain at least 8 characters.',
        951983354: 'This password is entirely numeric.',
    }

    response = client.post(reverse('RegisterView'), body, format='json')
    assert response.status_code == 401
    assert response.json().get('errors')[0] == errors[password]
@pytest.mark.django_db
def test_successful_registration():
    client = APIClient()
    body = {
        'username': 'JohnDoe',
        'password': 'StrongPassword123!',
        'email': 'johndoe@example.com',
    }
    response = client.post(reverse('RegisterView'), body, format='json')
    assert response.status_code == 201
    assert response.json() == {
    "username": "JohnDoe",
    "detail": "User created successfully"
    }
    qs = User.objects.filter(email='johndoe@example.com')
    assert qs.exists()
