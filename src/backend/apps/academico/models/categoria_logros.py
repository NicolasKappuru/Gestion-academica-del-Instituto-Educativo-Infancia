from django.db import models

class Categoria_logros(models.Model):
    id_categoria_logros = models.AutoField(primary_key=True)    
    nombre_categoria = models.CharField(max_length=50) 
    descripcion_categoria = models.CharField(max_length=250) 
    
    class Meta:
        db_table = 'Categoria_logros'

    #GETTERS

    def get_id_categoria_logros(self):
        return self.id_categoria_logros

    def get_nombre_categoria(self):
        return self.nombre_categoria

    def get_descripcion_categoria(self):
        return self.descripcion_categoria

    #SETTERS
    
    def set_nombre_categoria(self, value):
        self.nombre_categoria = value

    def set_descripcion_categoria(self, value):
        self.descripcion_categoria = value
