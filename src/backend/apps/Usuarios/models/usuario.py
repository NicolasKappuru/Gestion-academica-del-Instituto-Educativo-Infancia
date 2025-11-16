# apps/usuarios/models/usuario.py
from django.contrib.auth.models import User
from django.db import models
from .persona import Persona  

class Usuario(models.Model):
    ROLES = [
        ('acudiente', 'Acudiente'),
        ('profesor', 'Profesor'),
        ('administrador_academico', 'Administrador Académico'),
        ('administrador_usuarios', 'Administrador de Usuarios'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="usuarios")
    role = models.CharField(max_length=30, choices=ROLES)

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return f"{self.user.username} ({self.persona.primer_nombre})"
