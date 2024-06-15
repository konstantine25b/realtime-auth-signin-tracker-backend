from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    sign_in_count = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.username 