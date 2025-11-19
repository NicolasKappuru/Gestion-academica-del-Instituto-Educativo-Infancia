from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .persona import Persona

class Usuario(models.Model):

    codigo_usuario = models.CharField(
    max_length=20,
    primary_key=True,  
    )

    ROLES = [
        ('acudiente', 'Acudiente'),
        ('profesor', 'Profesor'),
        ('administrador_academico', 'Administrador Académico'),
        ('administrador_usuarios', 'Administrador de Usuarios'),
    ]

    ROLE_DIGITS = {
        'acudiente': '1',
        'profesor': '2',
        'administrador_academico': '3',
        'administrador_usuarios': '4',
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="usuarios")
    role = models.CharField(max_length=30, choices=ROLES)

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return f"{self.codigo_usuario} ({self.persona.primer_nombre})"

    def save(self, *args, **kwargs):
        # Generar solo si no existe
        if not self.codigo_usuario:
            year = timezone.now().year
            role_digit = self.ROLE_DIGITS[self.role]

            # Contar usuarios creados este año
            count_year = Usuario.objects.filter(
                codigo_usuario__startswith=str(year)
            ).count() + 1

            # Construir el código
            self.codigo_usuario = f"{year}{role_digit}{count_year:03d}"

        # Asignar el username del auth_user
        if self.user.username != self.codigo_usuario:
            self.user.username = self.codigo_usuario
            self.user.save()

        super().save(*args, **kwargs)
