from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
import openpyxl
from attendance.models import Batch, Course, Student,Subject,Teacher,Attendance,SubjectResult
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime


@login_required
def teacher_home(request):
    return render(request,'teacher/home.html')

@login_required
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

@login_required
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
                result,created = SubjectResult.objects.update_or_create(
                    student_id=student,
                    subject_id=subject,
                    defaults={'obtained_marks': obtained_marks, 'total_marks': total_marks}
                )
                result.save()

        messages.success(request, "Results added successfully!")
        return redirect('add_student_result')
    return render(request, 'teacher/add_result.html', {'subjects': subjects, 'students': students})

def view_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.all()
    batches = Batch.objects.all()
    
    # Initialize variables to avoid UnboundLocalError
    selected_course = None
    selected_subject = None
    selected_batch = None
    selected_date = None
    subjects = Subject.objects.filter()  # Default subject list
    
    attendance_records = []

    if request.method == 'POST':
        selected_course = request.POST.get('course')
        selected_subject = request.POST.get('subject')
        selected_batch = request.POST.get('batch')
        selected_date = request.POST.get('date')

        students = Student.objects.filter(course_id=selected_course, batch=selected_batch)

        for student in students:
            attendance = Attendance.objects.filter(
                student=student, subject_id=selected_subject, batch_id=selected_batch, date=selected_date
            ).first()
            
            attendance_records.append({
                'student_name': student.user.get_full_name(),
                'is_present': attendance.is_present if attendance else 'Absent',
                'date': attendance.date if attendance else 'N/A',
                'created_at': attendance.created_at if attendance else 'N/A',
                'updated_at': attendance.updated_at if attendance else 'N/A',
                })
    return render(request, 'teacher/view_attendance.html', {
        'courses': courses,
        'batches': batches,
        'subjects': subjects,
        'attendance_records': attendance_records,
        'selected_course': selected_course,
        'selected_subject': selected_subject,
        'selected_batch': selected_batch,
        'selected_date': selected_date
    })

def export_attendance_excel(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    selected_course = request.GET.get('course')
    selected_subject = request.GET.get('subject')
    selected_batch = request.GET.get('batch')
    selected_date = request.GET.get('date')

    if not all([selected_course, selected_subject, selected_batch, selected_date]):
        messages.error(request, "Please select all filters before exporting.")
        return redirect('view_attendance')

    # Fetch attendance records
    students = Student.objects.filter(course_id=selected_course, batch=selected_batch)
    
    # Create a new workbook and add a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Attendance Records"

    # Add headers
    sheet.append(["Student Name", "Attendance Status", "Date", "Created At", "Updated At"])

    for student in students:
        attendance = Attendance.objects.filter(
            student=student, subject_id=selected_subject, batch_id=selected_batch, date=selected_date
        ).first()

        # Convert timezone-aware datetime to naive datetime and format as string
        created_at = (localtime(attendance.created_at).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') 
                      if attendance and attendance.created_at else "N/A")

        updated_at = (localtime(attendance.updated_at).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') 
                      if attendance and attendance.updated_at else "N/A")

        sheet.append([
            student.user.get_full_name(),
            attendance.is_present if attendance else "Absent",
            selected_date,
            created_at,
            updated_at,
        ])

    # Auto-adjust column width
    for column_cells in sheet.columns:
        max_length = 0
        col_letter = column_cells[0].column_letter  # Get column letter (A, B, C, etc.)
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2  # Add extra padding
        sheet.column_dimensions[col_letter].width = adjusted_width

    # Prepare response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename=\"Attendance_{selected_date}.xlsx\"'
    workbook.save(response)

    return response