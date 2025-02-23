from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE = [
        ('student','student'),
        ('teacher','teacher'),
    ]
    user_type = models.CharField(max_length=10,choices = USER_TYPE)

    def __str__(self):
        return f'{self.username} ({self.user_type})'