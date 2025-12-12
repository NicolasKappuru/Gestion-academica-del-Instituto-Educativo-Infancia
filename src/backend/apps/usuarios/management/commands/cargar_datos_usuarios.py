# apps/usuarios/management/commands/cargar_usuarios.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
import random

from apps.usuarios.models.persona import Persona
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.profesor import Profesor
from apps.usuarios.models.administrador_academico import Administrador_academico
from apps.usuarios.models.administrador_de_usuarios import Administrador_de_usuarios
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.estudiante import Estudiante


class Command(BaseCommand):
    help = "Crea 1 acudiente, 1 profesor, 1 admin académico, 1 admin usuarios y 1 estudiante vinculado al acudiente."

    def random_nit(self):
        length = random.randint(8, 10)
        start = 10 ** (length - 1)
        end = (10 ** length) - 1
        return random.randint(start, end)

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # ---- PERSONAS A CREAR ----
        personas_info = [
            {"role": "acudiente", "nombre": "Carlos", "apellido": "Ramirez", "email": "carlos.ramirez@example.com"},
            {"role": "profesor", "nombre": "Laura", "apellido": "Gomez", "email": "laura.gomez@example.com"},
            {"role": "administrador_academico", "nombre": "Ana", "apellido": "Martinez", "email": "ana.martinez@example.com"},
            {"role": "administrador_usuarios", "nombre": "Jorge", "apellido": "Lopez", "email": "jorge.lopez@example.com"},
            {"role": "estudiante", "nombre": "Mateo", "apellido": "Fernandez", "email": None},
        ]

        created_personas = []

        # ---- CREAR PERSONAS ----
        for info in personas_info:
            persona = Persona.objects.create(
                primer_nombre=info["nombre"],
                segundo_nombre="",
                primer_apellido=info["apellido"],
                segundo_apellido="",
                NIT=self.random_nit()
            )
            created_personas.append((persona, info["role"], info["email"]))

        # ---- CREAR INSTANCIAS DE ROLES ----
        acudiente_obj = None

        for persona, role, email in created_personas:
            if role == "estudiante":
                continue

            # Crear usuario de Django
            user = User.objects.create(
                username=f"temp_{persona.id_persona}",
                email=email,
                is_active=True
            )
            user.set_password("1234")
            user.save()

            # Crear objeto concreto según el rol
            if role == "acudiente":
                acudiente_obj = Acudiente.objects.create(id_persona=persona)

            elif role == "profesor":
                Profesor.objects.create(id_persona=persona)

            elif role == "administrador_academico":
                Administrador_academico.objects.create(id_persona=persona)

            elif role == "administrador_usuarios":
                Administrador_de_usuarios.objects.create(id_persona=persona)

            # Crear Usuario (tu tabla)
            user_model = Usuario(
                user=user,
                persona=persona,
                role=role
            )
            user_model.save()  # genera codigo_usuario y actualiza username

        # ---- CREAR ESTUDIANTE Y VINCULARLO AL ACUDIENTE ----
        estudiante_persona = [p for p, r, e in created_personas if r == "estudiante"][0]

        Estudiante.objects.create(
            id_persona=estudiante_persona,
            fecha_nacimiento=timezone.now().date(),
            acudiente=acudiente_obj,   # aquí se vincula
            grupo=None
        )

        self.stdout.write(self.style.SUCCESS("Datos creados correctamente."))
