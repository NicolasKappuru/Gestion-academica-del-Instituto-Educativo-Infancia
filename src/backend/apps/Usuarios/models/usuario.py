# apps/usuarios/models/usuario.py
from django.contrib.auth.models import User
from django.db import models
from .persona import Persona

class Usuario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="usuarios")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
            db_table = 'Usuario'
            
    def __str__(self):
        return f"{self.user.username} ({self.persona.primer_nombre})"
    