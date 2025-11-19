from django.db import models
from .persona import Persona

class Infante_aspirante(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,   
        db_column='id_persona',  
    )

    
    fecha_nacimiento = models.DateField()
    
    class Meta:
            db_table = 'Infante_aspirante'
