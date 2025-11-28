# apps/usuarios/api/solicitudes.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.solicitudes.models.solicitud import Solicitud
from apps.academico.models.grado import Grado

class ListadoSolicitudes(APIView):
  
    def post(self, request):
        try:
            page = int(request.data.get("page", 1))
            page_size = int(request.data.get("page_size", 10))

            qs = Solicitud.objects.select_related(
                "acudiente_aspirante__id_persona",
                "infante_aspirante"
            ).order_by("id_solicitud")

            total = qs.count()

            inicio = (page - 1) * page_size
            fin = inicio + page_size
            pagina = qs[inicio:fin]

            data = []
            for s in pagina:
                # Nombre aspirante tomado desde la persona vinculada al acudiente
                persona = getattr(s.get_acudiente_aspirante(), "id_persona", None)
                if persona:
                    aspirante_nombre = f"{persona.get_primer_nombre()} {persona.get_primer_apellido()}"
                else:
                    aspirante_nombre = "Sin nombre"

                # intentamos obtener cupos desde Grado por nombre_grado (si existe)
                cupos = None
                try:
                    grado_obj = Grado.objects.filter(nombre_grado=s.grado_aplicar).first()
                    if grado_obj:
                        cupos = int(grado_obj.get_cupos_grado())
                except Exception:
                    cupos = None

                data.append({
                    "id": s.get_id_solicitud(),
                    "aspirante": aspirante_nombre,
                    "grado": s.get_grado_aplicar(),
                    "cupos": cupos,
                    "estado": s.get_estado_solicitud()
                })

            return Response({
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
                "solicitudes": data
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

