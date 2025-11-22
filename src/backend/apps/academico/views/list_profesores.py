from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.usuarios.models.profesor import Profesor

@method_decorator(csrf_exempt, name='dispatch')
class ListarProfesores(APIView):

    def get(self, request):

        try:
            profesores = Profesor.objects.all()

            data = []
            for p in profesores:
                persona = p.id_persona

                data.append({
                    "id_persona": persona.id_persona,
                    "nombre": f"{persona.primer_nombre} {persona.segundo_nombre}",
                    "apellido": f"{persona.primer_apellido} {persona.segundo_apellido or ''}"
                })

            return Response({"profesores": data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
