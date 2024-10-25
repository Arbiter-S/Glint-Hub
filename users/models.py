from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): #TODO: Add email verification with the required fields
    email = models.EmailField(unique=True)
