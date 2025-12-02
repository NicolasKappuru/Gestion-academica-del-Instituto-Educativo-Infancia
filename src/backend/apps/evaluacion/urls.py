from django.urls import path
from .views.list_estudiantes_grupo import ListEstudiantesGrupo
from .views.list_evaluacion_estudiante import ListEvaluacionEstudiante
from .views.generar_boletin import GenerarBoletin

urlpatterns = [
    path('listadoEstudiantesGrupo/', ListEstudiantesGrupo.as_view(), name="listadoEstudiantesGrupo"),
    path('listEvaluacionEstudiante/', ListEvaluacionEstudiante.as_view(), name="listEvaluacionEstudiante"), 
    path('generarBoletin/', GenerarBoletin.as_view(), name="generarBoletin"), 
]
