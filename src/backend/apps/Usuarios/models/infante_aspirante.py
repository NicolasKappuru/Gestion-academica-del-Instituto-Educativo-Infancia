from django.db import models
from .persona import Persona

class Infante_aspirante(Persona):
    fecha_nacimiento = models.DateField()

    class Meta:
            db_table = 'Infante_aspirante'
