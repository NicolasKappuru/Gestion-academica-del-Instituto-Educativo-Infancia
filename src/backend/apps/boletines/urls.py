from django.urls import path
from .views.list_estudiantes_boletines import ListadoEstudiantesBoletines

urlpatterns = [
    path('listadoEstudiantesBoletines/', ListadoEstudiantesBoletines().as_view(), name='listadoEstudiantesBoletines'),
]
