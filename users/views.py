# 3rd party library imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

# local imports
from .serializers import UserRegisterSerializer
from carts.models import Cart

User = get_user_model()


# TODO: Simple JWT has a listed security issue. Learn more about it and see if you can find an alternative

class UserRegisterView(CreateAPIView):
    """
    Creates a new User object.

    Request Body:
        username (str): username for the new user
        password (str): password for the new user

    Returns:
        201 Created: Username and a success message
        400 Bad Request: If the username is not unique.
        401 Unauthorized: If password is not validated.
    """
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        # user and cart creation
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        email = serializer.data.get('email')
        try:
            validate_password(password=password)
            user = User.objects.create_user(username=username, password=password, email=email)
            Cart.objects.create(user=user)
            body = {'username': username, 'detail': 'User created successfully'}
            status = 201
        except ValidationError as error:
            body = {'detail': 'Password validation failed', 'errors': error}
            status = 401

        headers = self.get_success_headers(serializer.data)

        return Response(data=body, status=status, headers=headers)
