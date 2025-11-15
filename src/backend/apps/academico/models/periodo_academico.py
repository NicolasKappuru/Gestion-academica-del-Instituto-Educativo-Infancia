from django.db import models

class Periodo_academico(models.Model):
    anio = models.PositiveIntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        db_table = 'Periodo_academico'

    