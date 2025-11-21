from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.solicitudes.models.solicitud import Solicitud
from apps.academico.models.grado import Grado
from apps.academico.models.grupo import Grupo
from apps.usuarios.models.estudiante import Estudiante
from apps.usuarios.models.acudiente import Acudiente


class AceptarSolicitud(APIView):

    @transaction.atomic
    def post(self, request):
        solicitud_id = request.data.get("id_solicitud")

        if not solicitud_id:
            return Response(
                {"error": "Falta id_solicitud"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ----------------------------------------------------
            # 1. Obtener solicitud
            # ----------------------------------------------------
            solicitud = Solicitud.objects.select_related(
                "infante_aspirante__id_persona",
                "acudiente_aspirante__id_persona"
            ).get(id_solicitud=solicitud_id)

            grado_nombre = solicitud.grado_aplicar

            # ----------------------------------------------------
            # 2. Buscar grado
            # ----------------------------------------------------
            grado = Grado.objects.get(nombre_grado=grado_nombre)

            # ----------------------------------------------------
            # 3. Validar cupos grado
            # ----------------------------------------------------
            if grado.cupos_grado <= 0:
                return Response(
                    {"error": "No hay cupos disponibles en el grado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ----------------------------------------------------
            # 4. Buscar grupo disponible
            # ----------------------------------------------------
            grupo = Grupo.objects.filter(
                grado=grado,
                cupos_grupo__gt=0
            ).order_by("id_grupo").first()

            if not grupo:
                return Response(
                    {"error": "No hay grupos con cupos disponibles"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ----------------------------------------------------
            # 5. CREAR ACUDIENTE REAL
            # ----------------------------------------------------
            acudiente_asp = solicitud.acudiente_aspirante

            # Verificar si ya existe
            acudiente_real, creado = Acudiente.objects.get_or_create(
                id_persona=acudiente_asp.id_persona
            )

            # ----------------------------------------------------
            # 6. Crear Estudiante desde Infante_aspirante
            # ----------------------------------------------------
            infante = solicitud.infante_aspirante
            persona_infante = infante.id_persona

            # Validar si ya existe estudiante
            if Estudiante.objects.filter(id_persona=persona_infante).exists():
                return Response(
                    {"error": "La persona ya está registrada como estudiante"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            estudiante = Estudiante.objects.create(
                id_persona=persona_infante,
                fecha_nacimiento=infante.fecha_nacimiento,
                acudiente=acudiente_real,
                grupo=grupo
            )

            # ----------------------------------------------------
            # 7. Restar cupos a grado y grupo
            # ----------------------------------------------------
            grado.cupos_grado -= 1
            grado.save()

            grupo.cupos_grupo -= 1
            grupo.save()

            # ----------------------------------------------------
            # 8. Cambiar estado de solicitud
            # ----------------------------------------------------
            solicitud.estado_solicitud = "Aceptada"
            solicitud.save()

            return Response({
                "ok": True,
                "estado": "Aceptada",
                "id_estudiante": estudiante.id_persona.id_persona,
                "id_acudiente": acudiente_real.id_persona.id_persona,
                "grupo_asignado": grupo.nombre_grupo
            })

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "Solicitud no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
