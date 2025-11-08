# apps/usuarios/models/estudiante.py
from django.db import models
from .persona import Persona
from .acudiente import Acudiente

class Estudiante(models.Model):
    models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,          
        related_name='estudiante'        
    )
    fecha_nacimiento = models.DateField()
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.SET_NULL,  # si borras al acudiente, el estudiante sigue existiendo
        null=True,
        related_name='estudiantes'  # permite acceder a los estudiantes desde el acudiente
    )
    class Meta:
        db_table = 'Estudiante'
