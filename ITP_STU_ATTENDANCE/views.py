from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from attendance.forms import UserRegisterForm, StudentRegisterForm, TeacherRegisterForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from attendance.models import User,Student,Teacher

def Base(request):
    return render(request, 'base.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.user_type == 'STUDENT':
                    return redirect('student_home')
                elif user.user_type == 'TEACHER':   
                    return redirect('teacher_home')
                elif user.user_type == 'ADMIN':
                    return redirect('admin_home')
                else:
                    return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    user_form = UserRegisterForm()
    student_form = StudentRegisterForm()
    teacher_form = TeacherRegisterForm()

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  
            user.user_type = user_form.cleaned_data.get('user_type')
            user.save()
            
            # print(f"User {user.username} created with user_type: {user.user_type}")

            if user.user_type == 'STUDENT':
                student = student_form.save(commit=False)
                student.user = user
                student.save()
            
            elif user.user_type == 'TEACHER':
                teachers = teacher_form.save(commit=False)
                teachers.user = user
                teachers.save()

            login(request, user)
            return redirect('login')
    return render(request, 'register.html', {'user_form': user_form})
    
def user_logout(request):
    logout(request)
    return redirect('login')