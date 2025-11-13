from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            # Creamos el token JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login correcto",
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            return Response({
                "error": "Credenciales inválidas"
            }, status=status.HTTP_401_UNAUTHORIZED)
