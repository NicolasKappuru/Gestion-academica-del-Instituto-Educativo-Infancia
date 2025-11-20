from django.urls import path
from apps.solicitudes.views.list_solicitudes import ListadoSolicitudes

urlpatterns = [
    path("listarSolicitudes/", ListadoSolicitudes.as_view(), name="listarSolicitudes"),
]
