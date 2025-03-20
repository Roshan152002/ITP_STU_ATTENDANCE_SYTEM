from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Student,SubjectResult,Attendance

@login_required
def student_home(request):
    return render(request, 'student/home.html')


def view_attendance(request):
    student = get_object_or_404(Student, user=request.user)
    attendances = Attendance.objects.filter(student=student)
    return render(request,'student/view_attendance.html',{'attendances':attendances,'student':student})
def view_result(request):
    student = get_object_or_404(Student, user=request.user)
    results = SubjectResult.objects.filter(student_id=student)
    return render(request,'student/view_result.html',{'results':results,'student':student})