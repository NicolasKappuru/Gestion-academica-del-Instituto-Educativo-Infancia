# apps/usuarios/models/estudiante.py
from django.db import models
from .persona import Persona
from .acudiente import Acudiente

class Estudiante(Persona):
    fecha_nacimiento = models.DateField()
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.CASCADE,
        related_name='estudiantes'
    )
    class Meta:
        db_table = 'Estudiante'
