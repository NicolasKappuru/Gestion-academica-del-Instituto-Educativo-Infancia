from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.academico.models.periodo_academico import Periodo_academico
from apps.academico.models.grado import Grado
from apps.academico.models.grupo import Grupo

class ListadoGruposPorPeriodo(APIView):

    def post(self, request):
        anio = request.data.get("anio")

        if not anio:
            return Response({"error": "Falta el año del periodo académico"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            periodo = Periodo_academico.objects.get(anio=anio)

            grados = Grado.objects.filter(periodo_acadmico=periodo)

            grupos = Grupo.objects.filter(grado__in=grados)

            data = []
            for g in grupos:
                profesor = g.get_profesor_director()

                if profesor and profesor.get_id_persona():
                    persona = profesor.get_id_persona()
                    profesor_data = {
                        "nombre": persona.get_primer_nombre(),
                        "apellido": persona.get_primer_apellido()
                    }
                else:
                    profesor_data = None


                data.append({
                    "id": g.get_id_grupo(),
                    "nombre": g.get_nombre_grupo(),
                    "grado": g.get_grado().get_nombre_grado() if g.get_grado() else None,
                    "profesor_director": profesor_data
                })



            return Response({"grupos": data}, status=status.HTTP_200_OK)

        except Periodo_academico.DoesNotExist:
            return Response({"error": "Periodo académico no encontrado"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
