from django.urls import path
from .views.list_grupos import ListadoGruposPorPeriodo

urlpatterns = [
    path('listadoGruposPeriodo/', ListadoGruposPorPeriodo().as_view(), name='listadoGruposPeriodo'),
]
