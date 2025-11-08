# apps/usuarios/models/acudiente.py
from django.db import models
from .persona import Persona

class Acudiente(models.Model):
    models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,          
        related_name='acudiente'        
    )
    
    class Meta:
        db_table = 'Acudiente'

    def agregar_estudiante(self, estudiante):
            estudiante.acudiente = self
            estudiante.save()