from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def student_home(request):
    return render(request, 'student/home.html')