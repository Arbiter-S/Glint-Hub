# 3rd party library imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from secrets import randbelow
from rest_framework.response import Response
from .serializers import EmailCodeSerializer


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

def validate_user_id_match(request, kwargs):
    """
    Validates if the authenticated user and the user for which verification is being attempted match.

    Args:
        request: request object
        kwargs: included url parameters

    Returns: user and user id

    """

    user = request.user
    user_id = user.id
    requested_user_id = kwargs.get('id')
    if user_id != requested_user_id:
        raise PermissionDenied('You are not allowed to handle verification for another user')
    return user, user_id


class VerifyEmailInitiate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user, user_id = validate_user_id_match(request, kwargs)
        if user.is_email_verified:
            return Response(status=400, data={'message': 'Email is already verified'})

        # avoid too many requests and verified users
        if not cache.get(f'verify_email_{user_id}'):
            # Generate a verification code
            verification_code = randbelow(900000) + 100000
            cache.set(f'verify_email_{user_id}', verification_code, 60*5) # 5 minutes
            send_mail('Verification code', "Hello. This email is being sent to verify your email"
                                           " in GlintHub if you have not requested verification please ignore this."
                                           f"your code: {verification_code}", 'verification@glinthub.com',
                      [user.email])

            return Response(status=200, data={'message': 'verification code has been emailed successfully'})
        else:
            return Response(status=400, data={'message': 'A verification code has already been sent.'
                                                         ' Please retry in a few minutes'})
    def post(self, request, *args, **kwargs):
        user, user_id = validate_user_id_match(request, kwargs)
        if user.is_email_verified:
            return Response(status=400, data={'message': 'Email is already verified'})

        serializer = EmailCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = int(serializer.validated_data.get('code'))

        if cache.get(f'verify_email_{user_id}') == code:
            user.is_email_verified = True
            user.save()
            return Response(status=200, data={'message': 'Email has been verified successfully'})
        else:
            return Response(status=400, data={'message': 'Invalid verification code'})




