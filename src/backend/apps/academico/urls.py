from django.urls import path
from .views.list_grupos import ListadoGruposPorPeriodo
from .views.list_profesores import ListarProfesores
from .views.asignar_profesor import AsignarProfesor

urlpatterns = [
    path('listadoGruposPeriodo/', ListadoGruposPorPeriodo.as_view(), name='listadoGruposPeriodo'),
    path('listarProfesores/', ListarProfesores.as_view(),   name="listarProfesores"),
    path('asignarProfesor/', AsignarProfesor.as_view(), name="asignarProfesor"),
]
