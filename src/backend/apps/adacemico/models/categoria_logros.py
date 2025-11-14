from django.db import models

class Categoria_logros(models.Model):
    id_categoria_logros = models.AutoField(primary_key=True)    
    nombre_categoria = models.CharField(max_length=50) 
    descripcion_categoria = models.CharField(max_length=250) 
    
    class Meta:
        db_table = 'Categoria_logros'