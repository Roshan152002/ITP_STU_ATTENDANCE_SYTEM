from django.shortcuts import render ,redirect
from .forms import UserRegisterForm , StudendentRegisterForm , TeacherRegisterForm
# Create your views here.

def register(request):
    user_form = UserRegisterForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False) # commit=False means that it will not save the data in the database
            user.save()

            if user.user_type == 'student':
                student_form = StudendentRegisterForm(request.POST,request.FILES)
                if student_form.is_valid():
                    student = student_form.save(commit=False)
                    student.user = user
                    student.save()
            
            elif user.user_type == 'teacher':
                teacher_form = TeacherRegisterForm(request.POST)
                if teacher_form.is_valid():
                    teacher = teacher_form.save(commit=False)
                    teacher.user = user
                    teacher.save()

    return render(request,'attendance/register.html',{'user_form':user_form})

                
                