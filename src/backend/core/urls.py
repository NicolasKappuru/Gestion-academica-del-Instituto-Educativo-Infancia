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
    path('api/', include('apps.evaluacion.urls')),
    path('api/citaciones/', include('apps.citaciones.urls')),
    path('api/restablecer/', include('apps.restablecer_contrasena.urls')),
]

