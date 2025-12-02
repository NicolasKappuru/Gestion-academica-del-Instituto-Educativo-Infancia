from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.profesor import Profesor
from apps.usuarios.models.estudiante import Estudiante
from apps.boletines.models.boletin import Boletin
from apps.academico.models.evaluacion import Evaluacion
from apps.academico.models.periodo_academico import Periodo_academico

import logging
import json


@method_decorator(csrf_exempt, name='dispatch')
class GenerarBoletin(APIView):

    def post(self, request):
        logger = logging.getLogger(__name__)

        # ===== LEER DATA UNA SOLA VEZ =====
        data = request.data

        username       = data.get("username")
        id_estudiante  = data.get("id_estudiante")
        evaluaciones   = data.get("evaluaciones", [])

        # === LOGS SEGUROS ===
        logger.warning("📥 DATA RECIBIDA")
        logger.warning(json.dumps(data, indent=2, ensure_ascii=False))

        if not username or not id_estudiante:
            return Response(
                {"error": "Faltan username o id_estudiante"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            """
            1) Profesor
            """
            usuario = Usuario.objects.select_related("persona").get(
                user__username=username
            )
            profesor = Profesor.objects.get(id_persona=usuario.persona)

            nombre_profesor = (
                f"{usuario.persona.primer_nombre} "
                f"{usuario.persona.primer_apellido}"
            )

            """
            2) Estudiante
            """
            estudiante = Estudiante.objects.get(pk=id_estudiante)

            """
            3) Período académico actual
            """
            periodo = Periodo_academico.objects.order_by("-anio").first()
            if not periodo:
                return Response(
                    {"error": "No existe período académico"},
                    status=status.HTTP_404_NOT_FOUND
                )

            """
            4) Boletín existente
            """
            boletin = Boletin.objects.get(
                estudiante=estudiante,
                periodo_academico=periodo
            )

            boletin.profesor_director = nombre_profesor
            boletin.save()

            """
            5) Actualizar evaluaciones
            """
            actualizadas = 0

            for item in evaluaciones:

                id_eval = item.get("id_evaluacion")

                if not id_eval:
                    continue

                try:
                    evaluacion = Evaluacion.objects.get(
                        id_evaluacion=id_eval,
                        boletin=boletin
                    )
                except Evaluacion.DoesNotExist:
                    continue

                evaluacion.evaluacion_corte1 = item.get("corte1")
                evaluacion.evaluacion_corte2 = item.get("corte2")
                evaluacion.evaluacion_corte3 = item.get("corte3")
                evaluacion.save()
                
                actualizadas += 1

            return Response(
                {
                    "msg": "Boletín actualizado correctamente",
                    "evaluaciones_actualizadas": actualizadas
                },
                status=status.HTTP_200_OK
            )

        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

        except Profesor.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Boletin.DoesNotExist:
            return Response({"error": "Boletín no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error("❌ ERROR EN GENERAR BOLETÍN", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
