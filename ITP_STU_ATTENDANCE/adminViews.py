from email.headerregistry import Address
from operator import gt
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Student, Subject,User,Course,Teacher,Batch


# Create your views here.
@login_required(login_url='/')
def admin_home(request):
    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    
    return render(request,'admin/home.html',{'stu_count':student_count,'t_count':teacher_count,'c_count':course_count,'sub_count':subject_count})


def student_list(request):
    students = Student.objects.all()
    return render(request,'admin/students.html',{'students':students})

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
    return render(request, 'admin/addTeacher.html',{'messages': messages})


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



