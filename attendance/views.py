from django.shortcuts import render, redirect
from .forms import UserRegisterForm, StudentRegisterForm, TeacherRegisterForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):
    user_form = UserRegisterForm()
    student_form = StudentRegisterForm()
    teacher_form = TeacherRegisterForm()

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        student_form = StudentRegisterForm(request.POST, request.FILES)
        teacher_form = TeacherRegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # i don't but without this student details are not saving
            user.save()

            if user.user_type == 'student' and student_form.is_valid():
                student = student_form.save(commit=False)
                student.user = user
                student.save()
            
            elif user.user_type == 'teacher' and teacher_form.is_valid():
                teachers = teacher_form.save(commit=False)
                teachers.user = user
                teachers.save()

            login(request, user)
            return redirect('dashboard')
    return render(request, 'attendance/register.html', {
        'user_form': user_form,
        'student_form': student_form,
        'teacher_form': teacher_form
    })



@login_required
def dashboard(request):
    user = request.user 

    if user.user_type == 'student':
        context = {
            "user_type": "student",
        }

    elif user.user_type == 'teacher':

        context = {
            "user_type": "teacher",

        }

    return render(request, "dashboards/student.html", context)
    

                
                