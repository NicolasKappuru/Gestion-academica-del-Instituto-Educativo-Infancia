from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from apps.usuarios.models.usuario import Usuario
from .utils import enviar_correo_restablecimiento

class ValidarDatosView(APIView):
    def post(self, request):
        codigo_usuario = request.data.get('codigo_usuario')
        email_ingresado = request.data.get('email')

        try:
            usuario = Usuario.objects.get(codigo_usuario=codigo_usuario)
            # IntentoRestablecimiento logic removed to handle attempts on frontend
            
            # Validar email
            if usuario.get_user().email != email_ingresado:
                mensaje = "Datos incorrectos"
                # Simplemente retornamos error, el frontend contara los intentos
                return Response({'error': mensaje, 'bloqueado': False}, status=status.HTTP_400_BAD_REQUEST)

            # Datos válidos
            
            # Usar generador estándar
            user = usuario.get_user()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # (Opcional) Guardamos timestamp en intento para meras estadísticas, pero la validez la da el token mismo
            # (Opcional) Guardamos timestamp en intento para meras estadísticas, pero la validez la da el token mismo
            # intento.save() <- Removed

            # Enviar correo
            # En entorno real o local, usamos la variable de entorno para el dominio
            frontend_url = settings.FRONTEND_URL.rstrip('/')
            
            # Construimos el enlace apuntando al archivo HTML estático tal cual existe en la estructura
            # Ruta relativa: restablecer_contraseña/ingresar_nueva_contraseña/ingresar_nueva_contraseña.html
            link = f"https://instituto-educativo-infancia.onrender.com/restablecer_contraseña/ingresar_nueva_contraseña/ingresar_nueva_contraseña.html?token={token}&uid={uid}"
            
            enviado = enviar_correo_restablecimiento(usuario, link)
            
            if not enviado:
                return Response({'error': 'Error al enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Revisar el correo electrónico'}, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            # Por seguridad, no decimos si el usuario existe o no, pero para el flujo exacto del diagrama
            # Si el usuario no existe, tecnicamente son "Datos incorrectos".
            # Simulamos el delay o fallo genérico.
            return Response({'error': 'Datos incorrectos', 'intentos': 1, 'bloqueado': False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Error de conexión a la BD'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidarContrasenaView(APIView):
    def post(self, request):
        # Aceptamos uid y token (Estándar) O codigo_usuario y token (Legacy/Fallback si necesario, pero priorizamos uid)
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        
        # Parametros legacy por si acaso front manda codigo_usuario en vez de uid (aunque actualizaremos front)
        codigo_usuario = request.data.get('codigo_usuario') 

        password_1 = request.data.get('password_1')
        password_2 = request.data.get('password_2')

        try:
            user = None
            usuario = None
            
            if uidb64:
                try:
                    uid = force_str(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                    usuario = Usuario.objects.get(user=user)
                except (TypeError, ValueError, OverflowError, User.DoesNotExist, Usuario.DoesNotExist):
                    user = None
            
            elif codigo_usuario:
                 # Fallback busqueda por codigo
                 usuario = Usuario.objects.get(codigo_usuario=codigo_usuario)
                 user = usuario.get_user()
            
            if not user or not usuario:
                 return Response({'error': 'Usuario no válido'}, status=status.HTTP_404_NOT_FOUND)

            # IntentoRestablecimiento logic removed
            # Obtener intento (solo si existiera logica adicional no bloqueante, pero eliminamos bloqueo)

            # 1. Verificar Token Estándar
            if not default_token_generator.check_token(user, token):
                 return Response({'error': 'El enlace de activación ha caducado'}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Validar coincidencia de passwords
            if password_1 != password_2:
                # El frontend maneja los intentos
                return Response({'error': 'Contraseña no coincide'}, status=status.HTTP_400_BAD_REQUEST)
 
            # Actualizar Contraseña
            user.set_password(password_1)
            user.save()
            
            # El token se invalida automaticamente por Django al cambiar el password
            
            return Response({'message': 'Contraseña actualizada'}, status=status.HTTP_200_OK)

        except Exception as e:
             return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
