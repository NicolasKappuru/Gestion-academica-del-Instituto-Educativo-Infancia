from django.db import models
from .periodo_academico import Periodo_academico

class Grado(models.Model):
    id_grado = models.AutoField(primary_key=True)
    nombre_grado = models.CharField(max_length=15) 
    cupos_grado = models.DecimalField(max_digits=2, decimal_places=0)
    periodo_acadmico = models.ForeignKey(
        Periodo_academico,
        db_column='anio'
    )
    
    class Meta:
        db_table = 'Grado'

