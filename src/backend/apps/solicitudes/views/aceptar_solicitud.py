from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.usuarios.models.solicitud import Solicitud

class AceptarSolicitud(APIView):
    """
    POST:
      - id_solicitud
    Cambia estado_solicitud a 'Aceptada'
    """
    @transaction.atomic
    def post(self, request):
        solicitud_id = request.data.get("id_solicitud")
        if not solicitud_id:
            return Response({"error": "Falta id_solicitud"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            s = Solicitud.objects.get(id_solicitud=solicitud_id)
            s.estado_solicitud = "Aceptada"
            s.save()
            return Response({"ok": True, "estado": s.estado_solicitud})
        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
