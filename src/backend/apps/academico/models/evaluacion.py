from django.db import models
from .logro import Logro
from apps.boletines.models.boletin import Boletin

class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    evaluacion_corte1 = models.CharField(max_length=15) 
    evaluacion_corte2 = models.CharField(max_length=15) 
    evaluacion_corte3 = models.CharField(max_length=15) 

    
    logro = models.ForeignKey(
        Logro,
        db_column='id_logro',
        on_delete=models.CASCADE
    )

    boletin = models.ForeignKey(
        Boletin,
        on_delete=models.SET_NULL,
        null=True,          
        blank=True,
        db_column='id_boletin',
        related_name='evaluaciones'
    )

    class Meta:
        db_table = 'Evaluacion'

