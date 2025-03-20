from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Student, Subject,User,Course,Teacher,Batch,Attendance
from openpyxl import Workbook
from datetime import datetime
from django.http import HttpResponse

# Create your views here.
@login_required
def admin_home(request):
    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    
    return render(request,'admin/home.html',{'stu_count':student_count,'t_count':teacher_count,'c_count':course_count,'sub_count':subject_count})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request,'admin/students.html',{'students':students})
@login_required
def student_add(request):
    courses = Course.objects.all()
    batches = Batch.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        course_id = request.POST.get('course')  # Get course ID from the form
        gender = request.POST.get('gender')
        roll_no = request.POST.get('rollno')
        batch_id = request.POST.get('batch')
        phonono = request.POST.get('phonono')
        profile = request.FILES.get('profile')
        
        
        user, created = User.objects.get_or_create(username=username, defaults={
            'first_name': firstname,
            'last_name': lastname,
            'email': email,
        })
        
        if created:
            user.set_password(password)
            messages.success(request, "Account created successfully!")
            user.save()
        else:
            messages.error(request,"User already exists")

        course = Course.objects.get(id=course_id) if course_id else None
        batch = Batch.objects.get(id=batch_id) if batch_id else None
        
        student = Student(
            user=user,
            course_id=course,
            gender=gender,
            email = email,
            roll_no=roll_no,
            batch=batch,
            phone_no=phonono,
            profile_pic=profile
        )
        student.save()

        return redirect('student_add')

    return render(request, 'admin/addStudent.html',{'courses': courses ,'batches':batches,'message':messages})
        
def student_edit(request, id):
    student = get_object_or_404(Student, user_id=id)
    user = student.user

    courses = Course.objects.all()
    batches = Batch.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        course_id = request.POST.get('course') 
        batch_id = request.POST.get('batch') 
        gender = request.POST.get('gender')
        roll_no = request.POST.get('rollno')
        batch = request.POST.get('batch')
        phonono = request.POST.get('phonono')
        profile = request.FILES.get('profile')
        
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()

        course = Course.objects.get(id=course_id) if course_id else None
        batch = Batch.objects.get(id=batch_id) if batch_id else None

        student.course = course
        student.batch = batch
        student.gender = gender
        student.roll_no = roll_no
        student.batch_name = batch
        student.phone_no = phonono
        if profile:  # Only update the profile if a new one is uploaded
            student.profile_pic = profile
        student.save()

        messages.success(request, 'Student Profile Updated Successfully!')
        return redirect('student_list')

    return render(request, 'admin/editStudent.html', {'courses': courses, 'student': student ,'batches':batches})

        
def student_detail(request, id):
    student = get_object_or_404(Student, user_id=id)
    user = student.user
    return render(request, 'admin/studentDetail.html', {'student': student, 'user': user})

def student_delete(request,id):
    student = get_object_or_404(Student, user_id=id)
    student.delete()
    return redirect('student_list')



def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request,'admin/teacherList.html',{'teachers':teachers})

def teacher_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phonono = request.POST.get('phonono')
        address = request.POST.get('address')
        department = request.POST.get('department')
        Profile = request.FILES.get('profile')
        
        
        user , created = User.objects.get_or_create(username=username, defaults={
            'first_name': firstname,
            'last_name': lastname,
            'email': email,
            'profile_pic':Profile,
            'user_type':'TEACHER',
        })
        
        if created:
            user.set_password(password)
            messages.success(request, "Account created successfully!")
            user.save()
        else:
            messages.error(request,"User already exists")

        teacher = Teacher(
            user=user,
            gender=gender,
            phone_no=phonono,
            address=address,
            department=department
        )
        teacher.save()
        return redirect('teacher_add')
    return render(request, 'admin/addTeacher.html',)


def teacher_edit(request,id):
    teacher = get_object_or_404(Teacher,user_id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phonono = request.POST.get('phonono')
        address = request.POST.get('address')
        department = request.POST.get('department')
        Profile = request.FILES.get('profile')

        user = teacher.user
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.profile_pic = Profile
        user.save()

        teacher.gender = gender
        teacher.phone_no = phonono
        teacher.address = address
        teacher.department = department
        teacher.save()

        messages.success(request, 'Teacher Profile Updated Successfully!')
        return redirect('teacher_list')

    return render(request, 'admin/editTeacher.html', {'teacher': teacher})


def teacher_detail(request,id):
    teacher = get_object_or_404(Teacher,user_id=id)
    return render(request, 'admin/teacherDetail.html', {'teacher': teacher})

def teacher_delete(request,id):
    teacher = get_object_or_404(Teacher,user_id=id)
    teacher.delete()
    return redirect('teacher_list')


def course_list(request):
    courses = Course.objects.all()
    return render(request,'admin/courseList.html',{'courses':courses})

def course_add(request):
    if request.method == 'POST':
        name = request.POST.get('course')
        course = Course(name=name)
        course.save()
        messages.success(request, "Course Added successfully!")
        return redirect('course_list')
    return render(request, 'admin/addCourse.html')


def course_edit(request,id):
    course = get_object_or_404(Course,id=id)
    if request.method == 'POST':
        name = request.POST.get('course')
        course.name = name
        course.save()
        messages.success(request, "Course Edited successfully!")
        return redirect('course_list')
    return render(request, 'admin/editCourse.html', {'course': course})

def course_delete(request,id):
    course = get_object_or_404(Course,id=id)
    course.delete()
    return redirect('course_list')


def subject_list(request):
    subjects = Subject.objects.all()
    return render(request,'admin/subjectList.html',{'subjects':subjects})

def subject_add(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        name = request.POST.get('subject')
        course_id = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        print(teacher_id,course_id)
        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(user=teacher_id)
        subject = Subject(name=name,course=course,teacher=teacher)
        subject.save()
        messages.success(request, "Subject Added successfully!")
        return redirect('subject_list')
    return render(request, 'admin/addSubject.html',{'courses':courses,'teachers':teachers})

def subject_edit(request,id):
    subject = get_object_or_404(Subject,id=id)
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        name = request.POST.get('subject')
        course_id = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(user=teacher_id)
        subject.name = name
        subject.course = course
        subject.teacher = teacher
        subject.save()
        messages.success(request, "Course edited successfully!")
        return redirect('subject_list')
    return render(request, 'admin/editSubject.html', {'subject': subject,'courses':courses,'teachers':teachers})

def subject_delete(request,id):
    subject = get_object_or_404(Subject,id=id)
    subject.delete()
    return redirect('subject_list')


def admin_view_attendance(request):
    courses = Course.objects.all()
    batches = Batch.objects.all()
    subjects = Subject.objects.all()
    students = None
    attendance_records = None
    selected_course = selected_subject = selected_batch = selected_date = None

    if request.method == 'GET' and 'fetch_data' in request.GET:
        selected_course = request.GET.get('course')
        selected_subject = request.GET.get('subject')
        selected_batch = request.GET.get('batch')
        selected_date = request.GET.get('date')

        students = Student.objects.filter(course_id=selected_course, batch=selected_batch)
        attendance_records = Attendance.objects.filter(
            subject_id=selected_subject, batch_id=selected_batch, date=selected_date
        )

    return render(request, "admin/view_attendance.html", {
        'courses': courses, 'batches': batches, 'subjects': subjects,
        'students': students, 'attendance_records': attendance_records,
        'selected_course': selected_course, 'selected_subject': selected_subject,
        'selected_batch': selected_batch, 'selected_date': selected_date
    })

def admin_export_attendance_excel(request):
    selected_course = request.GET.get('course')
    selected_subject = request.GET.get('subject')
    selected_batch = request.GET.get('batch')
    selected_date = request.GET.get('date')

    # Ensure all parameters are selected
    if not all([selected_course, selected_subject, selected_batch, selected_date]):
        messages.error(request, "Please select all filters before exporting.")
        return redirect('admin_view_attendance')

    # Convert selected_date from string to a date object
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()  
    except ValueError:
        messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
        return redirect('admin_view_attendance')

    # Fetch students in the selected course and batch
    students = Student.objects.filter(course_id=selected_course, batch=selected_batch)

    # Create a new workbook and add a worksheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Attendance Records"

    # Add headers
    sheet.append(["Student Name", "Attendance Status", "Date", "Created At", "Updated At"])

    for student in students:
        attendance = Attendance.objects.filter(
            student=student, subject_id=selected_subject, batch_id=selected_batch, date=selected_date
        ).first()

        # Handle cases where attendance is None
        if attendance:
            created_at = attendance.created_at.strftime('%Y-%m-%d %H:%M:%S') if attendance.created_at else "N/A"
            updated_at = attendance.updated_at.strftime('%Y-%m-%d %H:%M:%S') if attendance.updated_at else "N/A"
        else:
            created_at = "N/A"
            updated_at = "N/A"

        sheet.append([
            student.user.get_full_name(),
            "Present" if attendance and attendance.is_present else "Absent",
            selected_date.strftime('%Y-%m-%d'),
            created_at,
            updated_at,
        ])

    # Auto-adjust column width
    for column_cells in sheet.columns:
        max_length = max((len(str(cell.value)) if cell.value else 0) for cell in column_cells)
        adjusted_width = max_length + 2  # Add extra padding
        sheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

    # Prepare response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Attendance_{selected_date}.xlsx"'
    workbook.save(response)

    return response