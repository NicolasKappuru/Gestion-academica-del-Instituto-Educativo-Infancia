from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.academico.models.grupo import Grupo
from apps.usuarios.models.profesor import Profesor

@method_decorator(csrf_exempt, name='dispatch')
class AsignarProfesor(APIView):

    def post(self, request):
        id_grupo = request.data.get("grupo")
        id_profesor = request.data.get("profesor")

        if not id_grupo or not id_profesor:
            return Response({"error": "Datos incompletos"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            grupo = Grupo.objects.get(id_grupo=id_grupo)
            profesor = Profesor.objects.get(id_persona=id_profesor)

            # 1. Desasignar el profesor de otro grupo (si lo tiene)
            Grupo.objects.filter(profesor_director=profesor).update(profesor_director=None)

            # 2. Asignar a este grupo
            grupo.profesor_director = profesor
            grupo.save()

            return Response({"mensaje": "Profesor asignado"}, status=status.HTTP_200_OK)

        except Grupo.DoesNotExist:
            return Response({"error": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Profesor.DoesNotExist:
            return Response({"error": "Profesor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
