from django.db import models
from apps.usuarios.models.estudiante import Estudiante
from apps.academico.models.periodo_academico import Periodo_academico

class Boletin(models.Model):
    id_boletin = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=30) 
    profesor_director = models.CharField(max_length=250)

    estudiante = models.ForeignKey(
        Estudiante,
        db_column='id_persona_estudiante',
        related_name='boletines',
        null=True,
        on_delete=models.SET_NULL
    )

    periodo_academico = models.ForeignKey(
        Periodo_academico, 
        db_column="anio",
        on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'Boletin'

   