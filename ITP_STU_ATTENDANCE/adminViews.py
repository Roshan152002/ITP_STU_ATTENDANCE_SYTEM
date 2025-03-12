from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Student,User,Course


# Create your views here.
@login_required(login_url='/')
def admin_home(request):
    return render(request,'admin/home.html')


def student_list(request):
    students = Student.objects.all()
    return render(request,'admin/students.html',{'students':students})

def student_add(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        course_id = request.POST.get('course')  # Get course ID from the form
        gender = request.POST.get('gender')
        roll_no = request.POST.get('rollno')
        batch = request.POST.get('batch')
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

        
        student = Student(
            user=user,
            course_id=course,
            gender=gender,
            email = email,
            roll_no=roll_no,
            batch_name=batch,
            phone_no=phonono,
            profile_pic=profile
        )
        student.save()

        return redirect('student_list')

    return render(request, 'admin/addStudent.html',{'courses': courses})
        
def student_edit(request, id):
    student = get_object_or_404(Student, user_id=id)
    user = student.user

    courses = Course.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        course_id = request.POST.get('course')  
        gender = request.POST.get('gender')
        roll_no = request.POST.get('rollno')
        batch = request.POST.get('batch')
        phonono = request.POST.get('phonono')
        profile = request.FILES.get('profile')
        
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        # if password:
        #     user.set_password(password)
        user.save()

        course = Course.objects.get(id=course_id) if course_id else None

        student.course = course
        student.gender = gender
        student.roll_no = roll_no
        student.batch_name = batch
        student.phone_no = phonono
        if profile:  # Only update the profile if a new one is uploaded
            student.profile_pic = profile
        student.save()

        messages.success(request, 'Student Profile Updated Successfully!')
        return redirect('student_list')

    return render(request, 'admin/editStudent.html', {'courses': courses, 'student': student})

        
def student_detail(request, id):
    student = get_object_or_404(Student, user_id=id)
    user = student.user
    return render(request, 'admin/studentDetail.html', {'student': student, 'user': user})

def student_delete(request,id):
    student = get_object_or_404(Student, user_id=id)
    student.delete()
    return redirect('student_list')
