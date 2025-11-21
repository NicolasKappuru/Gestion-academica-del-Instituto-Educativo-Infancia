from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction

from apps.solicitudes.models.solicitud import Solicitud
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.persona import Persona


class CrearUsuarioAcudiente(APIView):

    def post(self, request):
        solicitud_id = request.data.get("id_solicitud")

        if not solicitud_id:
            return Response(
                {"error": "Debe enviar id_solicitud"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():

                # -------------------------------
                # 1. Obtener solicitud
                # -------------------------------
                solicitud = Solicitud.objects.select_related(
                    "acudiente_aspirante__id_persona"
                ).get(id_solicitud=solicitud_id)

                acudiente_asp = solicitud.acudiente_aspirante
                persona = acudiente_asp.id_persona
                email = acudiente_asp.correo_electronico_aspirante

                # -------------------------------
                # 2. Validar si la persona ya tiene usuario acudiente
                # -------------------------------
                if Usuario.objects.filter(persona=persona, role="acudiente").exists():
                    return Response(
                        {"error": "Ya existe un usuario acudiente para esta persona"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # -------------------------------
                # 3. Crear usuario Django
                # -------------------------------
                django_user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=str(persona.NIT)
                )
                django_user.is_active = True
                django_user.save()

                # -------------------------------
                # 4. Crear usuario del sistema
                # -------------------------------
                usuario = Usuario.objects.create(
                    user=django_user,
                    persona=persona,
                    role="acudiente"
                )
                usuario.save()

                # -------------------------------
                # 5. TERMINAR — NO crear Acudiente
                #    (ya existe esa persona como acudiente)
                # -------------------------------

                # -------------------------------
                # 6. Finalizar solicitud
                # -------------------------------
                solicitud.estado_solicitud = "Finalizada"
                solicitud.save()

                return Response(
                    {"message": "Usuario acudiente creado correctamente"},
                    status=status.HTTP_201_CREATED
                )

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "La solicitud no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
