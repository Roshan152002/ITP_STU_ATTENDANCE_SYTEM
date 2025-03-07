from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Base,name='BaseLayout'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('attendance/',include('attendance.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)