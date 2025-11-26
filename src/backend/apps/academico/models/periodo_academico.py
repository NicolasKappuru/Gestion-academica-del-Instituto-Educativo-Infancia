from django.db import models

class Periodo_academico(models.Model):
    anio = models.PositiveIntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    class Meta:
        db_table = 'Periodo_academico'

    #GETTERS

    def get_anio(self):
        return self.anio

    def get_fecha_inicio(self):
        return self.fecha_inicio

    def get_fecha_fin(self):
        return self.fecha_fin

    #SETTERS
    
    def set_fecha_inicio(self, value):
        self.fecha_inicio = value

    def set_fecha_fin(self, value):
        self.fecha_fin = value
