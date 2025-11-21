from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.solicitudes.models import Solicitud   # Ajusta si está en otro path


class ListadoCreacionAcudiente(APIView):

    def post(self, request):
        try:
            page = int(request.data.get("page", 1))
            page_size = int(request.data.get("page_size", 10))

            # 1. Filtrar solicitudes aceptadas
            solicitudes = (
                Solicitud.objects.filter(estado_solicitud="Aceptada")
                .order_by("id_solicitud")
            )

            total = solicitudes.count()

            # 2. Paginación
            inicio = (page - 1) * page_size
            fin = inicio + page_size
            solicitudes_page = solicitudes[inicio:fin]

            # 3. Armar estructura para la tabla
            data = []
            for sol in solicitudes_page:
                data.append({
                    "codigo_creacion": sol.id_solicitud,  # El código visible en la tabla
                    "id_solicitud": sol.id_solicitud,     # Igual, por si necesitas ID interno
                })

            return Response({
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
                "solicitudes": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
