from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from apps.usuarios.models.usuario import Usuario


class ListadoUsuarios(APIView):

    def post(self, request):
        role = request.data.get("role")
        page = int(request.data.get("page", 1))
        page_size = int(request.data.get("page_size", 10))

        if not role:
            return Response({"error": "Debe especificar un rol"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:

            usuarios = Usuario.objects.filter(role=role) \
                        .select_related("persona", "user") \
                        .order_by("persona__primer_nombre", "persona__primer_apellido")
            total = usuarios.count()


            # Paginado
            inicio = (page - 1) * page_size
            fin = inicio + page_size
            usuarios_pagina = usuarios[inicio:fin]

            data = []
            for u in usuarios_pagina:
                data.append({
                    "nombre": f"{u.persona.primer_nombre} {u.persona.primer_apellido}",
                    "estado": "Habilitado" if u.user.is_active else "Deshabilitado",
                    "id": u.codigo_usuario,
                    "id_user": u.user.id,
                })

            return Response({
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
                "usuarios": data
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
