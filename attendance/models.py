from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group,Permission
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    USER_TYPE = [
        ('ADMIN', 'Admin'),
        ('STUDENT','student'),
        ('TEACHER','teacher'),
    ]
    user_type = models.CharField(max_length=25,choices = USER_TYPE,default='STUDENT',null=False,blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Avoids conflict with auth.User.groups
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Avoids conflict with auth.User.user_permissions
        blank=True
    )

    def __str__(self):
        return f'{self.username} ({self.user_type})'
    
# class Admin(models.Model):
#     user = models.OneToOneField(User,)   
 
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='teacher_model')
    gender = models.CharField(max_length=20,default='male')
    phone_no = models.CharField(max_length=10,unique=True,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    joining_date = models.DateField(auto_now_add=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} (Teacher) from - {self.department} department'
class Course(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,related_name='teacher_subject')
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
   
    def __str__(self):
        return f'{self.name} - ({self.course})'
    
    
class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")
    
    def __str__(self):
        return f"{self.name} ({self.course.name})"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_model")
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.DO_NOTHING, null=True, blank=True,related_name="students") 
    roll_no = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    email = models.EmailField()
    gender = models.CharField(max_length=10,default='male',null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    profile_pic = models.FileField(upload_to='profile_pics/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)


    def __str__(self):
        return f"{self.user.username} - {self.roll_no} - ({self.batch.name})"

class Attendance(models.Model):
    PRESENTY_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(default=timezone.now)  # Default to today
    is_present = models.CharField(max_length=10, choices=PRESENTY_CHOICES, default='Absent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('student', 'subject', 'date')  # Prevent duplicate attendance for the same student

    def __str__(self):
        return f'{self.student.user.get_full_name()} - {self.subject.name} - {self.is_present} on {self.date}'

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='attendance_reports')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.attendance.student.user.get_full_name()} - {self.attendance.subject.name} - {self.attendance.is_present} on {self.attendance.date}'
    
    
class SubjectResult(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)
    obtained_marks = models.IntegerField()
    total_marks = models.IntegerField()
    created_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student_id', 'subject_id')
        
    def __str__(self):
        return f'{self.student_id.user.get_full_name()} - {self.subject_id.name} - {self.obtained_marks}/{self.total_marks}'

