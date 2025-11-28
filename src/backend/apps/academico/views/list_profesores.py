from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.usuarios.models.profesor import Profesor

class ListarProfesores(APIView):

    def get(self, request):

        try:
            profesores = Profesor.objects.all()

            data = []
            for p in profesores:
                persona = p.get_id_persona()

                data.append({
                    "id_persona": persona.get_id_persona(),
                    "nombre": f"{persona.get_primer_nombre()} {persona.get_segundo_nombre()}",
                    "apellido": f"{persona.get_primer_apellido()} {persona.get_segundo_apellido()}"
                })

            return Response({"profesores": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
