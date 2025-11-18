from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models.persona import Persona
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.estudiante import Estudiante
from apps.usuarios.models.profesor import Profesor
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.administrador_de_usuarios import Administrador_de_Usuarios 
from apps.usuarios.models.administrador_academico import Administrador_academico
from datetime import date
import random

class Command(BaseCommand):
    help = "Carga personas, acudientes, estudiantes, profesores y administradores con usuarios."

    def handle(self, *args, **kwargs):

        # ============================
        #  LIMPIAR TABLAS
        # ============================
        
        print("Usuarios auth:", User.objects.count())
        print("Registros Usuario:", Usuario.objects.count())

        # borrar registros dependientes primero
        Usuario.objects.all().delete()
        res = User.objects.all().delete()
        print("Resultado delete auth_user:", res)   # devuelve (n_registros, {'auth.User': n})
        Administrador_academico.objects.all().delete()
        Administrador_de_Usuarios.objects.all().delete()
        Profesor.objects.all().delete()
        Estudiante.objects.all().delete()
        Acudiente.objects.all().delete()
        Persona.objects.all().delete()

        # ============================
        #  LISTA DE NOMBRES
        # ============================
        nombres = [
            "Laura", "Marcos", "Lucia", "Daniel", "Sofia", "Andres", "Paula",
            "Camilo", "Isabella", "Felipe", "Valentina", "Mateo", "Juliana",
            "Sebastian", "Carolina", "Antonio", "Elena", "Pablo", "Martina",
            "Gabriel", "Sara", "Emilio", "Victoria", "Samuel", "Ana"
        ]

        apellidos = [
            "Garcia", "Paredes", "López", "Martinez", "Rojas", "Torres",
            "Castro", "Vargas", "Ramirez", "Cortes", "Navarro", "Quintero",
            "Mendoza", "Rivera"
        ]

        # ============================
        #  CREAR PERSONAS (35)
        # ============================
        personas = []
        for i in range(35):
            p = Persona.objects.create(
                primer_nombre=random.choice(nombres),
                segundo_nombre=random.choice(nombres),
                primer_apellido=random.choice(apellidos),
                segundo_apellido=random.choice(apellidos),
                NIT=random.randint(10000000, 99999999)
            )
            personas.append(p)

        self.stdout.write(self.style.SUCCESS(f"Personas creadas: {len(personas)}"))

        # ============================
        #   ASIGNACIONES MANUALES
        # ============================

        # 12 ACUDIENTES
        acudientes_personas = personas[:12]

        # 14 ESTUDIANTES
        estudiantes_personas = personas[12:26]

        # 8 PROFESORES
        profesores_personas = personas[26:34]

        # 1 persona con 4 roles → última
        super_persona = personas[34]

        fechas = [
            date(2021, 5, 10), date(2022, 3, 14), date(2023, 1, 22),
            date(2021, 7, 2),  date(2022, 11, 9), date(2023, 6, 30)
        ]

        # ----------------------------
        # CREAR ACUDIENTES
        # ----------------------------
        acudientes_objs = []
        for p in acudientes_personas:
            a = Acudiente.objects.create(id_persona=p)
            acudientes_objs.append(a)

        # =============================
        # ASIGNAR ACUDIENTES A ESTUDIANTES MANUALMENTE
        # =============================
        mapping = {
            0: [0, 1],       # acudiente 1 → estudiante 1,2
            1: [2],          # acudiente 2 → estudiante 3
            2: [3, 4],       # acudiente 3 → estudiante 4,5
            3: [5],          # ...
            4: [6],
            5: [7, 8],
            6: [9],
            7: [10],
            8: [11],
            9: [12],
            10: [13],
            11: []           # acudiente sin estudiante (válido)
        }

        estudiantes_objs = []

        for acud_idx, est_indices in mapping.items():
            for est_i in est_indices:
                p = estudiantes_personas[est_i]
                e = Estudiante.objects.create(
                    id_persona=p,
                    fecha_nacimiento=random.choice(fechas),
                    acudiente=acudientes_objs[acud_idx],
                    grupo=None
                )
                estudiantes_objs.append(e)

        # completar estudiantes no asignados (si alguno quedó sin entrar)
        for p in estudiantes_personas:
            if p not in [e.id_persona for e in estudiantes_objs]:
                e = Estudiante.objects.create(
                    id_persona=p,
                    fecha_nacimiento=random.choice(fechas),
                    acudiente=random.choice(acudientes_objs),
                    grupo=None
                )
                estudiantes_objs.append(e)

        # ----------------------------
        # CREAR PROFESORES
        # ----------------------------
        for p in profesores_personas:
            Profesor.objects.create(id_persona=p)

        # ----------------------------
        # CREAR ADMINISTRADORES
        # ----------------------------
        Administrador_academico.objects.create(id_persona=super_persona)
        Administrador_de_Usuarios.objects.create(id_persona=super_persona)
        Acudiente.objects.create(id_persona=super_persona)
        Profesor.objects.create(id_persona=super_persona)
        # =============================
        #  FUNCION CREAR USUARIO DJANGO
        # =============================
        def crear_user(persona, rol):
            username = f"{persona.primer_nombre.lower()}_{persona.NIT}_{rol}"
            email = f"{username}@correo.com"

            user = User.objects.create_user(
                username=username,
                password="1234",
                email=email,
                is_active=True
            )

            Usuario.objects.create(
                user=user,
                persona=persona,
                role=rol
            )

        # ----------------------------
        # CREAR USUARIOS PARA ROLES
        # ----------------------------

        # acudientes
        for a in acudientes_objs:
            crear_user(a.id_persona, "acudiente")

        # profesores
        for p in profesores_personas:
            crear_user(p, "profesor")

        # super persona (4 roles)
        for rol in ["acudiente", "profesor", "administrador_academico", "administrador_usuarios"]:
            crear_user(super_persona, rol)

        self.stdout.write(self.style.SUCCESS("Datos de usuarios creados correctamente."))

