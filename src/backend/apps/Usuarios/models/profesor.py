# apps/usuarios/models/profesor.py
from django.db import models
from .persona import Persona

class Profesor(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
        related_name='profesor'
    )

    class Meta:
        db_table = 'Profesor'
