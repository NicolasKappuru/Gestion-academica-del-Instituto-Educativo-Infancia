from django.db import models
from .persona import Persona

class Acudiente_aspirante(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
    )
    correo_electronico_aspirante = models.EmailField()

    class Meta:
            db_table = 'Acudiente_aspirante'
