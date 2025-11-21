from django.urls import path
from apps.solicitudes.views.list_solicitudes import ListadoSolicitudes
from apps.solicitudes.views.aceptar_solicitud import AceptarSolicitud

urlpatterns = [
    path("listarSolicitudes/", ListadoSolicitudes.as_view(), name="listarSolicitudes"),
    path("aceptarSolicitud/", AceptarSolicitud.as_view(), name="aceptarSolicitud"),
]
