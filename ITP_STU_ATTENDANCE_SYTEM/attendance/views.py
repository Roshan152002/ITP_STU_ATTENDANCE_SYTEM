from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core.mail import send_mail
from django.contrib import messages


from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model


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
                    "admin@example.com",
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('password_reset')

    else:
        form = PasswordResetForm()
    
    return render(request, 'attendance/password_reset.html', {'form': form})

import logging

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

        return render(request, "attendance/password_reset_confirm.html")
    else:
        messages.error(request, "Invalid password reset link!")
        return redirect("password_reset")



def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        student_form = StudentRegisterForm(request.POST, request.FILES)
        teacher_form = TeacherRegisterForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            # user.otp_created_at = now()
            user.save()
            send_mail(
                    "Your OTP Code",
                    f"Your OTP is: {otp}",
                    'mayurgholap.core12@gmail.com', 
                    [user.email],
                    fail_silently=False,
                )
            
            # Print OTP in terminal for debugging
            print(f"Generated OTP for {user.email}: {otp}")
            # Create Student or Teacher Profile after OTP verification
            if user.user_type == 'student':
                Student.objects.create(user=user, email=user.email)
            elif user.user_type == 'teacher':
                Teacher.objects.create(user=user, email=user.email)
            
            return redirect('verify_otp',user_id=user.id)
    else:
        user_form = UserRegisterForm()
        student_form = StudentRegisterForm()
        teacher_form = TeacherRegisterForm()

    return render(request, 'attendance/register.html', {
        'user_form': user_form,
        'student_form': student_form,
        'teacher_form': teacher_form
    })
    
def verify_otp(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        
        if user.otp == entered_otp:
            user.email_verified = True
            user.otp = None
            user.otp_created_at = None
            user.save()
            login(request, user)
            return redirect('user_login')
        else:
            return render(request, 'attendance/verify_otp.html', {'error': 'Invalid OTP', 'user_id': user_id})
    
    return render(request, 'attendance/verify_otp.html', {'user_id': user_id})
    
    

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or email.')
                return render(request, 'attendance/login.html', {'form': form})
            
            if not user.email_verified:
                messages.error(request, 'Your email is not verified. Please verify your email first.')
                return render(request, 'attendance/login.html', {'form': form})
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'attendance/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')




@login_required
def dashboard(request):
    user = request.user 

    if user.user_type == 'student':
        context = {
            "user_type": "student",
        }

    elif user.user_type == 'teacher':

        context = {
            "user_type": "teacher",

        }

    return render(request, "dashboards/student.html", context)
    

def get_user_profile(user):
    if user.user_type == 'student':
        return Student.objects.get(user=user)
    elif user.user_type == 'teacher':
        return Teacher.objects.get(user=user)
    return None

@login_required
def view_profile(request):
    profile = get_user_profile(request.user)
    return render(request, 'attendance/profile_handeling.html', {'profile': profile})

def edit_profile(request):
    user = request.user
    print(f"Logged-in user: {user} (User Type: {user.user_type})")

    if user.user_type == 'student':
        student = Student.objects.get(user=user)
        print(f"Student Data: {student.__dict__}")  # Print all stored data

        if request.method == 'POST':
            form = StudentRegisterForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = StudentRegisterForm(instance=student)
            print(f"Form Data Before Rendering: {form.initial}")  # Debug form data

    return render(request, 'attendance/edit_profile.html', {'form': form})
