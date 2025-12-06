from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import random
import datetime

from apps.usuarios.models.persona import Persona
from apps.usuarios.models.acudiente_aspirante import Acudiente_aspirante
from apps.usuarios.models.infante_aspirante import Infante_aspirante
from apps.solicitudes.models.solicitud import Solicitud


class Command(BaseCommand):
    help = "Genera 22 personas, 11 acudientes, 11 infantes y 11 solicitudes de prueba."

    def random_nit(self):
        length = random.randint(8, 10)
        start = 10 ** (length - 1)
        end = (10 ** length) - 1
        return random.randint(start, end)

    def random_fecha_nacimiento(self):
        """Fechas entre 2021 y 2023 (edades 2 a 4 años)."""
        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2023, 12, 31)
        delta = end_date - start_date
        random_days = random.randrange(delta.days)
        return start_date + datetime.timedelta(days=random_days)

    def handle(self, *args, **kwargs):
        with transaction.atomic():

            # ───────────────────────────────
            #   LISTAS BASE DE NOMBRES
            # ───────────────────────────────
            nombres = [
                "Felipe", "Martin", "Willian", "David", "Alejandro", "Gabriel", "Samuel",
                "Alan", "Alex", "Javier", "Alexander", "Viviana", "Paola",
                "Sofi", "Oscar", "Pedro", "Marieliza", "Marcela",
                "Sakura", "Jacinto", "Alberto", "Henry"
            ]

            apellidos = [
                "Chima", "Gomez", "Prieto", "Jhonmarcos", "Orosco", "Pesos",
                "Santos", "Vargas", "Lara", "Leal", "Duarte"
            ]

            # ───────────────────────────────
            #   1. Crear las 22 personas
            # ───────────────────────────────
            self.stdout.write("Creando 22 personas...")

            personas = []
            for i in range(22):
                p = Persona.objects.create(
                    primer_nombre=random.choice(nombres),
                    segundo_nombre=random.choice(nombres),
                    primer_apellido=random.choice(apellidos),
                    segundo_apellido=random.choice(apellidos),
                    NIT=self.random_nit()
                )
                personas.append(p)

            # separar 11 acudientes y 11 infantes
            acudientes_personas = personas[:11]
            infantes_personas = personas[11:]

            # ───────────────────────────────
            #   2. Crear acudiente_aspirante
            # ───────────────────────────────
            self.stdout.write("Creando 11 acudientes aspirantes...")

            acudientes = []
            for p in acudientes_personas:
                correo = f"{p.primer_nombre.lower()}.{p.primer_apellido.lower()}@example.com"
                a = Acudiente_aspirante.objects.create(
                    id_persona=p,
                    correo_electronico_aspirante=correo
                )
                acudientes.append(a)

            # ───────────────────────────────
            #   3. Crear infante_aspirante
            # ───────────────────────────────
            self.stdout.write("Creando 11 infantes aspirantes...")

            infantes = []
            for p in infantes_personas:
                fecha_nac = self.random_fecha_nacimiento()
                inf = Infante_aspirante.objects.create(
                    id_persona=p,
                    fecha_nacimiento=fecha_nac
                )
                infantes.append(inf)

            # ───────────────────────────────
            #   4. Crear solicitudes
            # ───────────────────────────────

            grados = ["Párvulos", "Caminadores", "Prejardín"]
            self.stdout.write("Creando 11 solicitudes...")

            for acudiente, infante in zip(acudientes, infantes):
                Solicitud.objects.create(
                    acudiente_aspirante=acudiente,
                    infante_aspirante=infante,
                    grado_aplicar=random.choice(grados),
                    estado_solicitud="Pendiente",
                )

            self.stdout.write(self.style.SUCCESS("¡Solicitudes de prueba generadas con éxito!"))
