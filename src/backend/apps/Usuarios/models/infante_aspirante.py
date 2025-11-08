from django.db import models
from .persona import Persona

class Infante_aspirante(models.Model):
    models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,          
        related_name='infante_aspirante'        
    )
    fecha_nacimiento = models.DateField()

    class Meta:
            db_table = 'Infante_aspirante'
