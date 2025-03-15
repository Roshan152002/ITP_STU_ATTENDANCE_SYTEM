from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Batch)
admin.site.register(Attendance)
# admin.site.register(Exam)
# admin.site.register(ExamSubmission)

