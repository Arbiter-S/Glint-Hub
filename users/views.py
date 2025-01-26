# 3rd party library imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import CharField, ListField
from logging import getLogger
from drf_spectacular.utils import extend_schema_view, extend_schema, inline_serializer

# local imports
from .serializers import UserRegisterSerializer, EmailCodeSerializer
from carts.models import Cart
from utils.verification import generate_code, cache_email_code

logger = getLogger(__name__)
User = get_user_model()


# TODO: Simple JWT has a listed security issue. Learn more about it and see if you can find an alternative

@extend_schema_view(
    post=extend_schema(
        summary="Register new user",
        description="""This endpoint creates a new user instance and assigns a cart instance to it.
        The password goes through default Django password validators before it can be used. Check this link for more info
        https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#s-enabling-password-validation""",
        responses={
            201: inline_serializer(
                name="UserCreationSuccessResponse",
                fields={
                    "username": CharField(),
                    "detail": CharField(default='User created successfully'),
                }
            ),
            400: inline_serializer(
                name="UserCreationBadRequestResponse",
                fields={
                    "field_name": CharField(default='user with this {field_name} already exists.'),
                }
            ),
            401: inline_serializer(
                name="UserCreationUnauthorizedResponse",
                fields={
                    "detail": CharField(default='Password validation failed'),
                    "errors": ListField(
                        child=CharField()
                    )
                }
            )
        }
    )
)
class UserRegisterView(CreateAPIView):
    # """
    # Creates a new User object.
    #
    # Request Body:
    #     username (str): username for the new user
    #     password (str): password for the new user
    #
    # Returns:
    #     201 Created: Username and a success message
    #     400 Bad Request: If the username is not unique.
    #     401 Unauthorized: If password is not validated.
    # """
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        # extracting validated data
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        # user and cart creation
        try:
            validate_password(password=password)
            user = User.objects.create_user(username=username, password=password, email=email)
            Cart.objects.create(user=user)
            body = {'username': username, 'detail': 'User created successfully'}
            status = 201

            logger.info(f"User and cart created successfully. username: {username} user_id: {user.pk}")
        except ValidationError as error:
            body = {'detail': 'Password validation failed', 'errors': error}
            status = 401

            logger.info(f"Password validation failed. username: {username}")

        headers = self.get_success_headers(serializer.data)

        return Response(data=body, status=status, headers=headers)



class VerifyEmail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_email_verified:
            logger.info(f"A verified user requested a verification code. user_id: {user.pk}")
            return Response(status=200, data={'message': 'Email is already verified'})

        # avoid too many requests
        if not cache.get(f'verify_email_{user.id}'):

            verification_code = generate_code()
            cache_email_code(user.id, verification_code)

            send_mail('Verification code', "Hello. This email is being sent to verify your email"
                                           " in GlintHub if you have not requested verification please ignore this."
                                           f"your code: {verification_code}", 'verification@glinthub.com',
                                [user.email])
            logger.info(f"Verification code emailed to user. user_id: {user.pk}")
            return Response(status=200, data={'message': 'verification code has been emailed successfully'})
        else:
            return Response(status=400, data={'message': 'A verification code has already been sent.'
                                                         ' Please retry in a few minutes'})
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_email_verified:
            logger.info(f"A verified user attempted to verify their email. username: {user.username}")
            return Response(status=200, data={'message': 'Email is already verified'})

        serializer = EmailCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = int(serializer.validated_data.get('code'))

        if cache.get(f'verify_email_{user.id}') == code:
            user.is_email_verified = True
            user.save()
            logger.info(f"A user verified their email. user_id: {user.pk}")
            return Response(status=200, data={'message': 'Email has been verified successfully'})
        else:
            return Response(status=400, data={'message': 'Invalid verification code'})
