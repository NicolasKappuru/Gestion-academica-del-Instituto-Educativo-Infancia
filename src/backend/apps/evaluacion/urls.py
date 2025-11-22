from django.urls import path
from .views.list_estudiantes_grupo import ListEstudiantesGrupo

urlpatterns = [
    path('listadoEstudiantesGrupo/', ListEstudiantesGrupo.as_view(), name="listadoEstudiantesGrupo"),
]
