from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.usuarios.models import Usuario

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            usuario = Usuario.objects.get(user=user)

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login correcto",
                "username": user.username,
                "role": usuario.get_role(),        
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "datos_personales": usuario.get_datos_personales()
            })

        return Response({"error": "Credenciales inválidas"}, status=401)
