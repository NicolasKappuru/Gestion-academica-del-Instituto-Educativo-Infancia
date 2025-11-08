# apps/usuarios/models/profesor.py
from django.db import models
from .persona import Persona

class Profesor(models.Model):
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  # Si se borra la persona, se borra el profesor
        primary_key=True,          # Hace que el campo 'persona' sea también la clave primaria
        related_name='profesor'    # Permite acceder desde Persona con persona.profesor
    )

    class Meta:
        db_table = 'Profesor'
