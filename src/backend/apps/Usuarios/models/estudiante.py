# apps/usuarios/models/estudiante.py
from django.db import models
from .persona import Persona

class Estudiante(Persona):
    fecha_nacimiento = models.DateField()
