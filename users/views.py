from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer

User = get_user_model()


# Create your views here.

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        # user creation
        username = serializer.data['username']
        password = serializer.data['password']
        validate_password(password=password)  # TODO: Find a way to make the errors specefic. Right now it's just 500
        User.objects.create_user(username=username, password=password)

        headers = self.get_success_headers(serializer.data)
        body = {'username': username, 'message': 'User created successfully'}
        return Response(data=body, status=status.HTTP_201_CREATED, headers=headers)
