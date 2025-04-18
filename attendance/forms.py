from django import forms
from .models import User, Student, Teacher
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['address', 'gender','course_id', 'phone_no', 'profile_pic']

class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone_no', 'address', 'department']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'gender', 'phone_no', 'address', 'profile_pic']

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone_no', 'address']