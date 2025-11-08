# apps/usuarios/models/profesor.py
from django.db import models
from .persona import Persona

class Profesor(Persona):
    
    class Meta:
        db_table = 'Profesor'
