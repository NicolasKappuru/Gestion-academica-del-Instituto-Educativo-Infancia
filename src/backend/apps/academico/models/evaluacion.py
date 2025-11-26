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

    #GETTERS
    
    def get_id_evaluacion(self):
        return self.id_evaluacion

    def get_evaluacion_corte1(self):
        return self.evaluacion_corte1

    def get_evaluacion_corte2(self):
        return self.evaluacion_corte2

    def get_evaluacion_corte3(self):
        return self.evaluacion_corte3

    def get_logro(self):
        return self.logro

    def get_boletin(self):
        return self.boletin

    #SETTERS

    def set_evaluacion_corte1(self, value):
        self.evaluacion_corte1 = value

    def set_evaluacion_corte2(self, value):
        self.evaluacion_corte2 = value

    def set_evaluacion_corte3(self, value):
        self.evaluacion_corte3 = value

    def set_logro(self, value):
        self.logro = value

    def set_boletin(self, value):
        self.boletin = value
