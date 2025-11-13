# apps/usuarios/models/administrador.py
from django.db import models
from .persona import Persona

class AdministradorAcademico(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
        related_name='administrador_academico'
    )

    class Meta:
        db_table = 'Administrador_academico'


