from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from attendance.models import Batch, Course, Student,Subject,Teacher,Attendance,SubjectResult
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def teacher_home(request):
    return render(request,'teacher/home.html')


def take_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses =Course.objects.all()
    batchs = Batch.objects.all()
    subjects = Subject.objects.filter(teacher=teacher)
    
    
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
            
            subject = get_object_or_404(Subject, id=selected_subject)
            batch = get_object_or_404(Batch, id=selected_batch)


            students = Student.objects.filter(course_id=selected_course , batch=selected_batch)
            for student in students:
                presenty = request.POST.get(f'presenty_{student.user.id}', 'Absent')  
                # print(presenty, student.user.first_name)
                attendace = Attendance.objects.create(student=student, subject=subject,batch=batch,teacher=teacher, date=selected_date, is_present=presenty)
                attendace.save()
    return render(request,"teacher/take_attendance.html",{'courses':courses,'subjects':subjects ,'batchs':batchs})


def add_student_result(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    subjects = Subject.objects.filter(teacher=teacher)
    students = Student.objects.filter(course_id__in=subjects.values_list('course', flat=True))

    if request.method == "POST":
        subject_id = request.POST.get('subject')

        subject = get_object_or_404(Subject, id=subject_id)

        for student in students:
            obtained_marks = request.POST.get(f'obtained_marks_{student.id}')
            total_marks = request.POST.get(f'total_marks_{student.id}')

            if obtained_marks and total_marks:
                obtained_marks = int(obtained_marks)
                total_marks = int(total_marks)

                if obtained_marks > total_marks:
                    messages.error(request, f"Obtained marks cannot be greater than total marks for {student.user.get_full_name()}.")
                    return render(request, 'teacher/add_result.html', {'subjects': subjects, 'students': students})

                # Update if exists, else create new result
                result = SubjectResult.objects.update_or_create(
                    student_id=student,
                    subject_id=subject,
                    defaults={'obtained_marks': obtained_marks, 'total_marks': total_marks}
                )
                result.save()

        messages.success(request, "Results added successfully!")
        return redirect('add_student_result')
    return render(request, 'teacher/add_result.html', {'subjects': subjects, 'students': students})