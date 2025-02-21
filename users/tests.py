import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache as cache_instance
from django.urls import reverse
from rest_framework.test import APIClient
from secrets import randbelow

User = get_user_model()


@pytest.mark.parametrize("password", ["asdfghjk", "prj8", 951983354])
@pytest.mark.django_db
def test_register_with_weak_password(client, password):
    body = {
        "username": "SomeRandomName",
        "password": password,
        "email": "testtest@gmail.com",
    }
    errors = {
        "asdfghjk": "This password is too common.",
        "prj8": "This password is too short. It must contain at least 8 characters.",
        951983354: "This password is entirely numeric.",
    }

    response = client.post(reverse("RegisterView"), body, format="json")
    assert response.status_code == 401
    assert response.json().get("errors")[0] == errors[password]


@pytest.mark.django_db
def test_registration_successful(client):
    body = {
        "username": "JohnDoe",
        "password": "StrongPassword123!",
        "email": "johndoe@example.com",
    }
    response = client.post(reverse("RegisterView"), body, format="json")
    assert response.status_code == 201
    assert response.json() == {
        "username": "JohnDoe",
        "detail": "User created successfully",
    }
    qs = User.objects.filter(email="johndoe@example.com")
    assert qs.exists()


@pytest.mark.django_db
def test_email_verification_initiate_successful(client):
    user = User.objects.create_user(
        username="JohnDoe", password="StrongPassword123!", email="johndoe@example.com"
    )
    client.force_authenticate(user)
    response = client.get(reverse("EmailVerification"))
    assert response.json() == {
        "message": "verification code has been emailed successfully"
    }


@pytest.mark.django_db
def test_email_verification_initiate_already_verified(client):
    user = User.objects.create_user(
        username="JohnDoe", password="StrongPassword123!", email="johndoe@example.com"
    )
    user.is_email_verified = True
    client.force_authenticate(user)
    response = client.get(reverse("EmailVerification"))
    assert response.json() == {"message": "Email is already verified"}
    assert response.status_code == 200


@pytest.fixture(scope="function")
def code_generation(client):
    user = User.objects.create_user(
        username="JohnDoe", password="StrongPassword123!", email="johndoe@example.com"
    )
    client.force_authenticate(user)
    response = client.get(reverse("EmailVerification"))
    assert cache_instance.get(f"verify_email_{user.id}") is not None
    return user


@pytest.mark.django_db
def test_email_verification_confirmation_successful(client, code_generation):
    user = code_generation
    code = cache_instance.get(f"verify_email_{user.id}")
    body = {"code": code}
    response = client.post(reverse("EmailVerification"), body, format="json")
    assert response.status_code == 200
    assert response.json() == {"message": "Email has been verified successfully"}
    assert user.is_email_verified is True


@pytest.mark.django_db
def test_email_verification_confirmation_failure(client, code_generation):
    user = code_generation
    body = {
        "code": randbelow(900000) + 100000
    }  # TODO: Should I make sure codes aren't the same?(1 in 900000)
    response = client.post(reverse("EmailVerification"), body, format="json")
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid verification code"}
    assert user.is_email_verified is False
