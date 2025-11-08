# apps/usuarios/models/administrador.py
from django.db import models
from .persona import Persona

class AdministradorDeUsuarios(Persona):
    
    class Meta:
        db_table = 'Administrador_de_usuarios'
