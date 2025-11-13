# apps/usuarios/models/administrador.py
from django.db import models
from .persona import Persona

class AdministradorDeUsuarios(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
        related_name='administrador_de_usuarios'
    )
    class Meta:
        db_table = 'Administrador_de_usuarios'
