from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group,Permission

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
 
class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='student_model',default='STUDENT')
    course_id = models.ForeignKey(Course,on_delete=models.DO_NOTHING,null=True,blank=True,default=None)
    gender = models.CharField(max_length=10,default='male',null=True,blank=True)
    roll_no = models.CharField(max_length=10)
    batch_name = models.CharField(max_length=100,null=False,blank=False)
    phone_no = models.CharField(max_length=10,unique=True,null=True,blank=True)
    email = models.EmailField()
    address = models.TextField(null=True,blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_pic = models.FileField(upload_to='profile_pics/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f'{self.user.username} - {self.roll_no}'

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


class Subject(models.Model):
    name = models.CharField(max_length=100,unique=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,related_name='teacher_subject')
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
   
    def __str__(self):
        return f'{self.name} - ({self.course})'
    

# class Attendance(models.Model):
#     presenty = [
#         ('present','present'),
#         ('absent','absent'),
#     ]

#     student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_attendance')
#     subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subject_attendance')
#     date = models.DateField(auto_now_add=True)
#     is_present = models.CharField(max_length=10,choices=presenty,default='absent')

#     class Meta:
#         ordering = ['-date']

#     def __str__(self):
#         return f'{self.student.user.username} - {self.subject.subject_name} -{self.is_present} on {self.date}'
    

# class Exam(models.Model):
#     title = models.CharField(max_length=255,unique=True)
#     subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='subject_exam')
#     teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='exam_conducted')
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     total_marks = models.IntegerField()

#     def __str__(self):
#         return f'{self.title} - {self.subject.subject_name} on {self.date} - {self.start_time} to {self.end_time}'


# class ExamSubmission(models.Model):
#     student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_exam_submission')
#     exam = models.ForeignKey(Exam,on_delete=models.CASCADE,related_name='exam_submission')
#     marks_obtained = models.IntegerField()
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     file = models.FileField(upload_to='exam_submissions/',null=True,blank=True)

#     class Meta:
#         unique_together = [('student','exam')]
#         ordering = ["-submitted_at"]

#     def __str__(self):
#         return f'{self.student.user.username} - {self.exam.title} - {self.marks_obtained}'
    
