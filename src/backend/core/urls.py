from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.login.urls')),  # 👈 aquí conectas tu app login

]
