from django.db import models
from .periodo_academico import Periodo_academico

class Grado(models.Model):
    id_grado = models.AutoField(primary_key=True)
    nombre_grado = models.CharField(max_length=15)
    cupos_grado = models.DecimalField(max_digits=2, decimal_places=0)
    periodo_acadmico = models.ForeignKey(
        Periodo_academico,
        db_column='anio',
        on_delete=models.SET_NULL,
        null=True
    )

    logros_grado = []


    def consultar_lista(self):
        self.logros_grado = list(self.logros.all())
        return self.logros_grado


    def agregar_lista(self, logro):
        logro.grado = self
        logro.save()
        self.consultar_logros()


    def eliminar_lista(self, id_logro):
        logro = Logro.objects.get(id_logro=id_logro, grado=self)
        logro.delete()
        self.consultar_logros()
        return True

    class Meta:
        db_table = 'Grado'

    # -----------------
    # GETTERS
    # -----------------
    def get_id_grado(self):
        return self.id_grado

    def get_nombre_grado(self):
        return self.nombre_grado

    def get_cupos_grado(self):
        return self.cupos_grado

    def get_periodo_acadmico(self):
        return self.periodo_acadmico

    # -----------------
    # SETTERS
    # -----------------
    def set_nombre_grado(self, value):
        self.nombre_grado = value

    def set_cupos_grado(self, value):
        self.cupos_grado = value

    def set_periodo_acadmico(self, value):
        self.periodo_acadmico = value
