from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    # TODO Check the issue with how django handles char fields and see how to implement a unique but nullable char field
    is_email_verified = models.BooleanField(default=False)
