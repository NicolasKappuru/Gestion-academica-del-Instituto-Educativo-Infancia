# apps/usuarios/models/administrador.py
from django.db import models
from .persona import Persona

class AdministradorAcademico(models.Model):
    models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,  
        primary_key=True,          
        related_name='administrador_academico'        
    )

    class Meta:
        db_table = 'Administrador_academico'


