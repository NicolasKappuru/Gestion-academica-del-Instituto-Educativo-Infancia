# apps/usuarios/models/acudiente.py
from django.db import models
from .persona import Persona

class Acudiente(Persona):
    
    class Meta:
        db_table = 'Acudiente'

    def agregar_estudiante(self, estudiante):
            estudiante.acudiente = self
            estudiante.save()