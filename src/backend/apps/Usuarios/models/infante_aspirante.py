from django.db import models
from .persona import Persona

class Infante_aspirante(Persona):
    fecha_nacimiento = models.DateField()
