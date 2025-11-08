from django.db import models
from .persona import Persona

class Acudiente_aspirante(models.Model):
    models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,          
        related_name='acudiente_aspirante'        
    )
    correo_electronico_aspirante = models.EmailField(unique=True)

    class Meta:
            db_table = 'Acudiente_aspirante'
