from django.db import models
from django.contrib.auth.models import AbstractUser, Group,Permission

# Create your models here.

class User(AbstractUser):
    USER_TYPE = [
        ('student','student'),
        ('teacher','teacher'),
    ]
    user_type = models.CharField(max_length=10,choices = USER_TYPE,default='student',null=False,blank=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Avoids conflict with auth.User.groups
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Avoids conflict with auth.User.user_permissions
        blank=True
    )

    def __str__(self):
        return f'{self.username} ({self.user_type})'