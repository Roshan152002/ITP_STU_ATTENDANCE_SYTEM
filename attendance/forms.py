from .models import User , Student , Teacher
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','user_type']

class StudendentRegisterForm(ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no','batch_name','phone_no','email','address','profile_pic']

class TeacherRegisterForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone_no','email','address','department']