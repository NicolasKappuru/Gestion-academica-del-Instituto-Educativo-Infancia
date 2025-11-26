from django.db import models
from .grado import Grado
from .categoria_logros import Categoria_logros

class Logro(models.Model):
    id_logro = models.AutoField(primary_key=True)
    concepto_logro = models.CharField(max_length=50)
    descripcion_logro = models.CharField(max_length=250)

    grado = models.ForeignKey(
        Grado,
        on_delete=models.SET_NULL,
        null=True,          
        blank=True,
        db_column='id_grado',
        related_name='logros'
    )     

    categoria_logros = models.ForeignKey(
        Categoria_logros,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='id_categoria_logros',
        related_name='logros'
    )

    class Meta:
        db_table = 'Logro'

    #GETTERS

    def get_id_logro(self):
        return self.id_logro

    def get_concepto_logro(self):
        return self.concepto_logro

    def get_descripcion_logro(self):
        return self.descripcion_logro

    def get_grado(self):
        return self.grado

    def get_categoria_logros(self):
        return self.categoria_logros

    #SETTERS
    
    def set_concepto_logro(self, value):
        self.concepto_logro = value

    def set_descripcion_logro(self, value):
        self.descripcion_logro = value

    def set_grado(self, value):
        self.grado = value

    def set_categoria_logros(self, value):
        self.categoria_logros = value
