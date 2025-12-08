from django.urls import path
from .views import ValidarDatosView, ValidarContrasenaView

urlpatterns = [
    path('validar-datos/', ValidarDatosView.as_view(), name='validar_datos'),
    path('validar-contrasena/', ValidarContrasenaView.as_view(), name='validar_contrasena'),
]
