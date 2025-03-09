from django.urls import path
from . import views
from attendance.views import custom_password_reset, custom_password_reset_confirm

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('verify_otp/<int:user_id>/',views.verify_otp, name='verify_otp'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
    
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password_reset/', custom_password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', custom_password_reset_confirm, name='password_reset_confirm'),
]