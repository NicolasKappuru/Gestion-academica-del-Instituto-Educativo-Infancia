# apps/usuarios/models/acudiente.py
from django.db import models
from .persona import Persona

class Acudiente(Persona):
    estudiantes = models.ManyToManyField('Estudiante', related_name='acudientes')

    def agregar_estudiante(self, acudido):
        self.estudiantes.add(acudido)
