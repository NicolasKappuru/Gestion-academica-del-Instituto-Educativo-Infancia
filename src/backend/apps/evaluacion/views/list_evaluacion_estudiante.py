from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.usuarios.models.estudiante import Estudiante
from apps.boletines.models.boletin import Boletin
from apps.academico.models.evaluacion import Evaluacion
from apps.academico.models.periodo_academico import Periodo_academico


@method_decorator(csrf_exempt, name='dispatch')
class ListEvaluacionEstudiante(APIView):

    def post(self, request):
        id_estudiante = request.data.get("id_estudiante")

        if not id_estudiante:
            return Response(
                {"error": "Falta id_estudiante"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # === 1. Estudiante ===
            estudiante = Estudiante.objects.select_related("id_persona").get(
                id_persona_id=id_estudiante
            )

            nombre_estudiante = (
                f"{estudiante.id_persona.primer_nombre} "
                f"{estudiante.id_persona.primer_apellido}"
            )

            # === 2. Periodo actual ===
            periodo = Periodo_academico.objects.order_by("-anio").first()

            if not periodo:
                return Response(
                    {"error": "No existe período académico"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # === 3. Boletín asociado ===
            boletin = Boletin.objects.get(
                estudiante=estudiante,
                periodo_academico=periodo
            )

            # === 4. Evaluaciones ===
            evaluaciones = Evaluacion.objects.filter(
                boletin=boletin
            ).select_related("logro")

            data = []

            for ev in evaluaciones:
                data.append({
                    "id_evaluacion": ev.id_evaluacion,
                    "id_logro": ev.logro.id_logro,
                    "logro": ev.logro.concepto_logro,
                    "descripcion": ev.logro.descripcion_logro,
                    "corte1": ev.evaluacion_corte1,
                    "corte2": ev.evaluacion_corte2,
                    "corte3": ev.evaluacion_corte3,
                })

            return Response({
                "estudiante": nombre_estudiante,
                "evaluaciones": data
            }, status=status.HTTP_200_OK)

        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no existe"}, status=status.HTTP_404_NOT_FOUND)

        except Boletin.DoesNotExist:
            return Response({"error": "No existe boletín para el estudiante"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
