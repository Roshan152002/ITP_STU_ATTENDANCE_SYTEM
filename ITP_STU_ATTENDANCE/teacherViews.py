from django.shortcuts import get_object_or_404, render
from attendance.models import Batch, Course, Student,Subject,Teacher,Attendance
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def teacher_home(request):
    return render(request,'teacher/home.html')


def take_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses =Course.objects.all()
    batchs = Batch.objects.all()
    subjects = Subject.objects.filter(teacher=teacher)
    
    students = [] 

    selected_course = None
    selected_subject = None
    selected_batch = None
    selected_date = None
    
    if request.method == 'POST':
        if 'fetch_data' in request.POST :
            selected_course = request.POST.get('course')
            selected_subject = request.POST.get('subject')
            selected_batch = request.POST.get('batch')
            selected_date = request.POST.get('date')


            students = Student.objects.filter(course_id=selected_course , batch=selected_batch)
            return render(request, "teacher/take_attendance.html",{'selected_course':selected_course,'courses':courses,'selected_subject':selected_subject,'subjects':subjects,'selected_date':selected_date,'students':students,'selected_batch':selected_batch,'batchs':batchs })

        elif 'attendance_submit' in request.POST:
            selected_course = request.POST.get('course')
            selected_subject = request.POST.get('subject')
            selected_batch = request.POST.get('batch')
            selected_date = request.POST.get('date')


            students = Student.objects.filter(course_id=selected_course , batch=selected_batch)
            for student in students:
                presenty = request.POST.get('presenty')
                print(presenty,student.user.first_name)
    return render(request,"teacher/take_attendance.html",{'courses':courses,'subjects':subjects ,'batchs':batchs})