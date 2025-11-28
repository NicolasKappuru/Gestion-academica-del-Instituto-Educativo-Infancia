from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.solicitudes.models.solicitud import Solicitud

class RechazarSolicitud(APIView):
   
    @transaction.atomic
    def post(self, request):
        solicitud_id = request.data.get("id_solicitud")

        if not solicitud_id:
            return Response(
                {"error": "Falta id_solicitud"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            solicitud = Solicitud.objects.get(id_solicitud=solicitud_id)
            acudiente_asp = solicitud.get_acudiente_aspirante()
            infante_asp = solicitud.get_infante_aspirante()
           
            acudiente_asp = solicitud.get_acudiente_aspirante()
            infante_asp = solicitud.get_infante_aspirante()

            infante_asp.delete()
            acudiente_asp.delete()

            solicitud.delete()

            return Response(
                {"ok": True, "mensaje": "Solicitud eliminada correctamente"},
                status=status.HTTP_200_OK
            )

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "Solicitud no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
