from django.urls import path
from .views import (
    ListarGruposView,
    ListarEstudiantesGrupoView,
    GestionarCitacionesView,
    ListarSolicitudesPendientesView,
    EnviarCitacionEntrevistaView
)


urlpatterns = [
    path('grupos/', ListarGruposView.as_view(), name='listar_grupos'),
    path('grupos/<int:id_grupo>/estudiantes/', ListarEstudiantesGrupoView.as_view(), name='listar_estudiantes_grupo'),
    path('enviar/', GestionarCitacionesView.as_view(), name='enviar_citaciones'),
    path('solicitudes/', ListarSolicitudesPendientesView.as_view(), name='listar_solicitudes'),
    path('entrevista/', EnviarCitacionEntrevistaView.as_view(), name='enviar_entrevista'),
]
