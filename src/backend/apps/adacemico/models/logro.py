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
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column='id_categoria_logros',
        related_name='logros'
    )

    class Meta:
        db_table = 'Logro'
