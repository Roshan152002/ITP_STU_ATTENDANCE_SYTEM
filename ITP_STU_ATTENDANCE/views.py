from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from attendance.forms import UserRegisterForm, StudentRegisterForm, TeacherRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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
            return redirect('login')
    return render(request, 'register.html', {
        'user_form': user_form,
        'student_form': student_form,
        'teacher_form': teacher_form
    })