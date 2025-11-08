# apps/usuarios/models/estudiante.py
from django.db import models
from .persona import Persona
from .acudiente import Acudiente

class Estudiante(Persona):
    fecha_nacimiento = models.DateField()
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.SET_NULL,  # si borras al acudiente, el estudiante sigue existiendo
        null=True,
        related_name='estudiantes'  # permite acceder a los estudiantes desde el acudiente
    )
    class Meta:
        db_table = 'Estudiante'
