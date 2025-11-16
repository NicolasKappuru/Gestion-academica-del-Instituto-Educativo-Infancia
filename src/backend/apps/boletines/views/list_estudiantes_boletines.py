from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.estudiante import Estudiante

@method_decorator(csrf_exempt, name='dispatch')
class ListadoEstudiantesBoletines(APIView):

    def post(self, request):

        username = request.data.get("username")

        if not username:
            return Response({"error": "Falta el username"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            usuario = Usuario.objects.get(user=user)
            persona = usuario.persona
            acudiente = Acudiente.objects.get(id_persona=persona)
            estudiantes = Estudiante.objects.filter(acudiente=acudiente)

            data = [
                {
                    "nombre": f"{est.id_persona.primer_nombre} {est.id_persona.primer_apellido}"
                }
                for est in estudiantes
            ]

            return Response({"estudiantes": data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        except Acudiente.DoesNotExist:
            return Response({"error": "La persona no es un acudiente"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
