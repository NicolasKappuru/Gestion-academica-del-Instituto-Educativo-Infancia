from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.usuarios.models.profesor import Profesor
from apps.academico.models.grupo import Grupo
from apps.usuarios.models.estudiante import Estudiante  # ajusta si está en otra app


@method_decorator(csrf_exempt, name='dispatch')
class ListEstudiantesGrupo(APIView):

    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response({"error": "Falta el username"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # === 1. Buscar profesor a través del usuario del sistema ===
            profesor = Profesor.objects.get(
                id_persona__usuarios__user__username=username
            )

            # === 2. Buscar grupo asignado ===
            grupo = Grupo.objects.filter(profesor_director=profesor).first()

            if not grupo:
                return Response(
                    {"error": "El profesor no tiene grupo asignado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # === 3. Buscar estudiantes del grupo ===
            estudiantes = Estudiante.objects.filter(grupo=grupo).select_related("id_persona")

            lista_estudiantes = [
                {
                    "nombre": f"{e.id_persona.primer_nombre} {e.id_persona.primer_apellido}"
                }
                for e in estudiantes
            ]

            # === 4. Respuesta ===
            return Response({
                "grupo": grupo.nombre_grupo,
                "estudiantes": lista_estudiantes
            }, status=status.HTTP_200_OK)

        except Profesor.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
