from django.urls import path
from .views.list_usuarios import ListadoUsuarios 
from .views.crear_usuario import CrearUsuario
from .views.habilitar_deshabilitar import HabilitarDeshabilitarUsuario
from .views.list_creacion_acudiente import ListadoCreacionAcudiente
urlpatterns = [
    path("listarUsuarios/", ListadoUsuarios.as_view(), name="listarUsuarios"),
    path("crearUsuario/", CrearUsuario.as_view(), name="crearUsuario"),
    path("habilitarDeshabilitar/", HabilitarDeshabilitarUsuario.as_view(), name="habilitarDeshabilitar"), 
    path("listarCreacionAcudientes/", ListadoCreacionAcudiente.as_view(), name="listarCreacionAcudientes"),
]
