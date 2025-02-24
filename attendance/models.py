from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group,Permission

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
    
class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='student_model')
    roll_no = models.CharField(max_length=10,unique=True)
    batch_name = models.CharField(max_length=100,null=False,blank=False)
    phone_no = models.CharField(max_length=10,unique=True,null=True,blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True,blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',null=True,blank=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f'{self.user.username} - {self.roll_no}'
