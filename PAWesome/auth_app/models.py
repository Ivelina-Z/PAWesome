from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    confirmation_token = models.CharField(blank=True, null=True)
