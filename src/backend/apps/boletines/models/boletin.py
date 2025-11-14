from django.db import models
from apps.usuarios.models.estudiante import Estudiante
from apps.adacemico.models.periodo_academico import Periodo_academico

class Boletin(models.Model):
    id_boletin = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=50) 
    profesor_director = models.CharField(max_length=250)

    estudiante = models.ForeignKey(
        Estudiante,
        db_column='id_persona_estudiante',
        related_name='boletines'
    )

    periodo_academico = models.ForeignKey(
        Periodo_academico, 
        db_column="anio",
    )
    
    class Meta:
        db_table = 'Boletin'

   