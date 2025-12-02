from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.usuarios.models.estudiante import Estudiante
from apps.boletines.models.boletin import Boletin


class ListadoBoletinesEstudiante(APIView):

    def post(self, request):

        id_persona = request.data.get("id_persona")

        if not id_persona:
            return Response({"error": "Falta id_persona del estudiante"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            estudiante = Estudiante.objects.get(id_persona=id_persona)

            boletines = Boletin.objects.filter(estudiante=estudiante)

            if not boletines.exists():
                return Response(
                    {"boletines": [], "mensaje": "El estudiante no tiene boletines"},
                    status=status.HTTP_200_OK
                )

            data = []

            for b in boletines:
                periodo = b.periodo_academico

                # Mostramos solo el año
                periodo_texto = periodo.anio

                data.append({
                    "id_boletin": b.id_boletin,
                    "periodo": periodo_texto
                })

            return Response({"boletines": data}, status=status.HTTP_200_OK)

        except Estudiante.DoesNotExist:
            return Response({"error": "Estudiante no encontrado"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("ERROR EN BOLETINES:", e)  # <-- Te mostrará el error REAL
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
