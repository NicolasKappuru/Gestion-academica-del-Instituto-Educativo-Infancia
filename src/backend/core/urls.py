from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.login.urls')),  
    path('api/', include('apps.formularios.urls')),
    path('api/', include('apps.boletines.urls')),
    path('api/', include('apps.academico.urls')),
    path('api/', include('apps.usuarios.urls')),
    path('api/', include('apps.solicitudes.urls')),
]
