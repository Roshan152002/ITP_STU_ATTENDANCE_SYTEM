from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from attendance.forms import UserRegisterForm, StudentRegisterForm, TeacherRegisterForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from attendance.models import User,Student,Teacher
from django.contrib import messages
from django.core.mail import send_mail
import random
from attendance.forms import StudentProfileForm,TeacherProfileForm

import logging
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from attendance.models import Course,Batch

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
                if user.user_type == 'STUDENT':
                    return redirect('student_home')
                elif user.user_type == 'TEACHER':   
                    return redirect('teacher_home')
                elif user.user_type == 'ADMIN':
                    return redirect('admin_home')
                else:
                    messages.error(request, "Invalid user type.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission. Please check your inputs.")
    
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    user_form = UserRegisterForm()
    
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)

        if user_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password1'])  
                user.user_type = user_form.cleaned_data.get('user_type')
                user.save()
                
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.save()
                
                send_mail(
                    "Your OTP Code",
                    f"Your OTP is: {otp}",
                    'DummyEmail7066@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                
                print(f"Generated OTP for {user.email}: {otp}")
                
                if user.user_type == 'STUDENT':
                    student = Student.objects.create(user=user, email=user.email)
                    student.save()
                
                elif user.user_type == 'TEACHER':
                    teacher = Teacher.objects.create(user=user)
                    teacher.save()
                
                messages.success(request, "Registration successful! Please verify your OTP.")
                return redirect('verify_otp', user_id=user.id)

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        
        else:
            messages.error(request, "Invalid form submission. Please check your inputs.")
    
    return render(request, 'register.html', {'user_form': user_form})
    
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    courses = Course.objects.all()
    batches = Batch.objects.all()
    data = User.objects.get(id=request.user.id)  # Get logged-in user

    if request.method == "POST":
        # Update User model fields
        data.first_name = request.POST.get('FirstName')
        data.last_name = request.POST.get('LastName')
        data.email = request.POST.get('Email')
        data.profile_pic = request.FILES.get('ProfilePicture')
        data.save()

        # Update Teacher fields if user is a TEACHER
        if data.user_type == 'TEACHER':
            teacher = Teacher.objects.get(user=data)
            teacher.phone_no = request.POST.get('PhoneNo')
            teacher.address = request.POST.get('Address')
            teacher.gender = request.POST.get('Gender')
            teacher.department = request.POST.get('Department')
            teacher.save()

        # Update Student fields if user is a STUDENT
        elif data.user_type == 'STUDENT':
            student = Student.objects.get(user=data)
            student.roll_no = request.POST.get('RollNo')
            student.phone_no = request.POST.get('PhoneNo')
            course_id = request.POST.get('course')
            if course_id:
                student.course_id = Course.objects.get(id=course_id)
            
            batch_id = request.POST.get('batch')
            if batch_id:
                student.batch_id = Batch.objects.get(id=batch_id)
            
            student.address = request.POST.get('Address')
            student.gender = request.POST.get('Gender')
            student.profile_pic = request.FILES.get('ProfilePicture')
            student.save()

        messages.success(request, 'Profile Updated Successfully')
        return redirect('profile')
    return render(request, 'profile.html', {'data': data,'courses': courses ,'batches':batches})

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"http://127.0.0.1:8000/reset/{uid}/{token}/"
                
                # Send Email (Print to terminal for testing)
                print(f"Password Reset Link: {reset_url}")  
                send_mail(
                    "Reset Your Password",
                    f"Click the link to reset your password: {reset_url}",
                    "DummyEmail7066@gmail.com",
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('password_reset')

    else:
        form = PasswordResetForm()
    
    return render(request, 'password_reset.html', {'form': form})


User = get_user_model()
logger = logging.getLogger(__name__)

def custom_password_reset_confirm(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except (User.DoesNotExist, ValueError, TypeError) as e:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")


            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect("password_reset_confirm", uidb64=uidb64, token=token)

            user.set_password(new_password)  
            user.save()  

            messages.success(request, "Password reset successful! You can now log in with your new password.")
            return redirect("user_login")

        return render(request, "password_reset_confirm.html")
    else:
        messages.error(request, "Invalid password reset link!")
        return redirect("password_reset")
    
def verify_otp(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        
        if user.otp == entered_otp:
            user.email_verified = True
            user.otp = entered_otp
            user.otp_created_at = None
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP', 'user_id': user_id})
    
    return render(request, 'verify_otp.html', {'user_id': user_id})
    
    
def edit_profile(request):
    user = request.user
    print(f"Logged-in user: {user} (User Type: {user.user_type})")

    # Determine user type and fetch the correct profile model
    if user.user_type == 'STUDENT':
        try:
            profile = Student.objects.get(user=user)
            form_class = StudentProfileForm
        except Student.DoesNotExist:
            return redirect('student_home')  # Redirect if student profile is missing

    elif user.user_type == 'TEACHER':
        try:
            profile = Teacher.objects.get(user=user)
            form_class = TeacherProfileForm
        except Teacher.DoesNotExist:
            return redirect('teacher_home')  # Redirect if teacher profile is missing

    else:
        return redirect('login')  # Redirect if user type is invalid

    # Handle POST request
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # return redirect('dashboard')  # Redirect after saving
    else:
        form = form_class(instance=profile)  # Pre-fill form with current data

    return render(request, 'edit_profile.html', {'form': form})
