from django.urls import path
from .views.list_estudiantes_boletines import ListadoEstudiantesBoletines
from .views.list_boletines_estudiante import ListadoBoletinesEstudiante
from .views.descargar_boletin import DescargarBoletin

urlpatterns = [
    path('listadoEstudiantesBoletines/', ListadoEstudiantesBoletines().as_view(), name='listadoEstudiantesBoletines'),
    path('listadoBoletinesEstudiante/', ListadoBoletinesEstudiante().as_view(), name="listadoBoletinesEstudiante"),
    path('descargar-boletin/', DescargarBoletin.as_view(), name="descargar-boletin"),
]
