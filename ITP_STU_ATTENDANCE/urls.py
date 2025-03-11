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
    path('admins/dashboard/',adminViews.admin_home,name='admin_home'),
    path('student/dashboard/',studentViews.student_home,name='student_home'),
    path('teacher/dashboard/',teacherViews.teacher_home,name='teacher_home'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('attendance/',include('attendance.urls')),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('verify_otp/<int:user_id>/',views.verify_otp, name='verify_otp'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)