# apps/usuarios/models/administrador.py
from django.db import models
from .persona import Persona

class Administrador_de_Usuarios(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
    )
    class Meta:
        db_table = 'Administrador_de_usuarios'
