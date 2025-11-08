from django.db import models
from .persona import Persona

class Acudiente_aspirante(Persona):
    correo_electronico_aspirante = models.EmailField(unique=True)

    class Meta:
            db_table = 'Acudiente_aspirante'
