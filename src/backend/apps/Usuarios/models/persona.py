# apps/usuarios/models/persona.py
from django.db import models
from .usuario import Usuario

class Persona(models.Model):
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    NIT = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
