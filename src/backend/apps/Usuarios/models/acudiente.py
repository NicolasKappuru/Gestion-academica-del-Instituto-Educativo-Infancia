# apps/usuarios/models/acudiente.py
from django.db import models
from .persona import Persona

class Acudiente(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
        related_name='acudiente'
    )
    
    class Meta:
        db_table = 'Acudiente'

    def agregar_estudiante(self, estudiante):
            estudiante.acudiente = self
            estudiante.save()