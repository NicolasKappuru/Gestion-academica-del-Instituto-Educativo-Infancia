from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction


class HabilitarDeshabilitarUsuario(APIView):

    def post(self, request):
        id_user = request.data.get("id_user")

        if not id_user:
            return Response(
                {"error": "Debe enviar id_user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                usuario = User.objects.filter(id=id_user).first()

                if not usuario:
                    return Response(
                        {"error": "Usuario no encontrado"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Alternar estado
                usuario.is_active = not usuario.is_active
                usuario.save()

                nuevo_estado = "Habilitado" if usuario.is_active else "Deshabilitado"

                return Response(
                    {
                        "message": "Estado actualizado",
                        "nuevo_estado": nuevo_estado
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
