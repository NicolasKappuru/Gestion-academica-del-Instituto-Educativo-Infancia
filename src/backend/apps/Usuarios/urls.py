from django.urls import path
from .views.list_usuarios import ListadoUsuarios 

urlpatterns = [
    path("listarUsuarios/", ListadoUsuarios.as_view(), name="listarUsuarios"),
]
