from django.urls import path
from . import views , adminViews , teacherViews , studentViews

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
]