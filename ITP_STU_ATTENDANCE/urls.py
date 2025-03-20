from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import adminViews
from . import studentViews
from . import teacherViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.user_login,name='login'),
    path('base/',views.Base,name='BaseLayout'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('verify_otp/<int:user_id>/',views.verify_otp, name='verify_otp'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    
    path('admins/dashboard/',adminViews.admin_home,name='admin_home'),
    path('admins/students/',adminViews.student_list,name='student_list'),
    path('admins/students/add/',adminViews.student_add,name="student_add"),
    path('admins/students/detail/<int:id>/',adminViews.student_detail,name="student_detail"),
    path('admins/students/update/<int:id>/',adminViews.student_edit,name="student_edit"),
    path('admins/students/delete/<int:id>/',adminViews.student_delete,name="student_delete"),
    
    path('admins/teachers/',adminViews.teacher_list,name='teacher_list'),
    path('admins/teacher/add/',adminViews.teacher_add,name="teacher_add"),
    path('admins/teacher/update/<int:id>/',adminViews.teacher_edit,name="teacher_edit"),
    path('admins/teacher/detail/<int:id>/',adminViews.teacher_detail,name="teacher_detail"),
    path('admins/teacher/delete/<int:id>/',adminViews.teacher_delete,name="teacher_delete"),
    
    path('admins/courses/',adminViews.course_list,name='course_list'),
    path('admins/courses/add/',adminViews.course_add,name="course_add"),
    path('admins/courses/update/<int:id>/',adminViews.course_edit,name="course_edit"),    
    path('admins/courses/delete/<int:id>/',adminViews.course_delete,name="course_delete"),
    
    path('admins/subjects/',adminViews.subject_list,name='subject_list'),
    path('admins/subjects/add/',adminViews.subject_add,name="subject_add"),
    path('admins/subjects/update/<int:id>/',adminViews.subject_edit,name="subject_edit"),
    path('admins/subjects/delete/<int:id>/',adminViews.subject_delete,name="subject_delete"),
    
    path('admin-panel/view-attendance/', adminViews.admin_view_attendance, name='admin_view_attendance'),
    path('admin-panel/exportAttendance/', adminViews.admin_export_attendance_excel, name="admin_export_attendance_excel"),
    
    
    path('teacher/dashboard/',teacherViews.teacher_home,name='teacher_home'),
    path('teacher/takeAttendance/',teacherViews.take_attendance,name='take_attendance'),
    path('teacher/student/result/',teacherViews.add_student_result,name='add_student_result'),
    path('teacher/viewAttendance/',teacherViews.view_attendance,name='teacher_view_attendance'),
    path('teacher/exportAttendance/', teacherViews.export_attendance_excel, name='export_attendance_excel'),
    
    path('student/dashboard/',studentViews.student_home,name='student_home'),
    path('student/viewAttendance/',studentViews.view_attendance,name='view_attendance'),
    path('student/viewResult/',studentViews.view_result,name='view_result'),
    path('attendance/',include('attendance.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)