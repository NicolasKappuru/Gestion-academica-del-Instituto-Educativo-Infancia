from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.utils import timezone
from apps.usuarios.models.usuario import Usuario
from .models import IntentoRestablecimiento
from .utils import enviar_correo_restablecimiento

class ValidarDatosView(APIView):
    def post(self, request):
        codigo_usuario = request.data.get('codigo_usuario')
        email_ingresado = request.data.get('email')

        try:
            usuario = Usuario.objects.get(codigo_usuario=codigo_usuario)
            intento, created = IntentoRestablecimiento.objects.get_or_create(usuario=usuario)

            # Verificar bloqueo
            if intento.esta_bloqueado():
                return Response({'error': 'Bloqueo por 5 minutos', 'bloqueado': True}, status=status.HTTP_403_FORBIDDEN)

            # Validar email
            if usuario.get_user().email != email_ingresado:
                intento.registrar_fallo_datos()
                mensaje = "Datos incorrectos"
                if intento.intentos_datos > 3:
                     return Response({'error': 'Bloqueo por 5 minutos', 'bloqueado': True}, status=status.HTTP_403_FORBIDDEN)
                
                return Response({'error': mensaje, 'intentos': intento.intentos_datos, 'bloqueado': False}, status=status.HTTP_400_BAD_REQUEST)

            # Datos válidos - Resetear intentos y Generar Token
            intento.reiniciar_intentos_datos()
            token = get_random_string(32)
            intento.token_validacion = token
            intento.fecha_token = timezone.now()
            intento.save()

            # Enviar correo
            frontend_url = request.build_absolute_uri('/frontend/restablecer/nueva_contrasena.html') # Ajustar ruta segun frontend real
            # Hack para desarrollo local si no está servido el frontend en el mismo puerto o estructura
            # Asumiremos una estructura relativa o que el frontend maneja el parametro ?token=...&uid=...
             # Mejor usamos una url relativa que el usuario pueda armar. 
             # Suponiendo que el frontend está en ../frontend/restablecer... 
             # El link debe llevar al archivo HTML que vamos a crear.
            
            # En un entorno real, esto seria una URL completa del frontend.
            # Vamos a asumir que el usuario corre esto localmente.
            # http://127.0.0.1:5500/src/frontend/restablecer/nueva_contrasena.html?token=...&id=...
            
            link = f"http://127.0.0.1:5500/src/frontend/restablecer_contraseña/ingresar_nueva_contraseña/ingresar_nueva_contraseña.html?token={token}&id={codigo_usuario}"
            
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
        codigo_usuario = request.data.get('codigo_usuario')
        token = request.data.get('token')
        password_1 = request.data.get('password_1')
        password_2 = request.data.get('password_2')

        try:
            usuario = Usuario.objects.get(codigo_usuario=codigo_usuario)
            intento = IntentoRestablecimiento.objects.get(usuario=usuario)

            # Verificar token (seguridad simple)
            if intento.token_validacion != token:
                 return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

            # Validar coincidencia
            if password_1 != password_2:
                intento.registrar_fallo_contrasena()
                if intento.intentos_contrasena > 3:
                     return Response({'error': 'Intentar más tarde', 'finalizar': True}, status=status.HTTP_403_FORBIDDEN)
                return Response({'error': 'Contraseña no coincide', 'intentos': intento.intentos_contrasena}, status=status.HTTP_400_BAD_REQUEST)

            # Validar intentos previos (si llegamos aqui coinciden, pero verificamos si no estaba ya bloqueado por intentos excesivos antes? 
            # El diagrama dice "Si excedieron los intentos -> Intentar mas tarde". 
            # Pero en mi logica arriba ya retorno error si excede.
            # Aqui es "Coinciden" -> Si han sido 3 intentos o menos -> Actualizar BD.
            
            if intento.intentos_contrasena > 3:
                 return Response({'error': 'Intentar más tarde', 'finalizar': True}, status=status.HTTP_403_FORBIDDEN)

            # Actualizar Contraseña
            user = usuario.user
            user.set_password(password_1)
            user.save()
            
            # Limpiar estado
            intento.reiniciar_intentos_contrasena() # O borrar token
            intento.token_validacion = None # Invalidar token usado
            intento.save()

            return Response({'message': 'Contraseña actualizada'}, status=status.HTTP_200_OK)

        except (Usuario.DoesNotExist, IntentoRestablecimiento.DoesNotExist):
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({'error': 'Error de conexión a la BD'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
