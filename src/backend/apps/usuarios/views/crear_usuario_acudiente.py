from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.solicitudes.models.solicitud import Solicitud
from apps.usuarios.models.usuario import Usuario
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.persona import Persona


class CrearUsuarioAcudiente(APIView):

    def post(self, request):
        solicitud_id = request.data.get("id_solicitud")

        if not solicitud_id:
            return Response(
                {"error": "Debe enviar id_solicitud"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():

                # -------------------------------
                # 1. Obtener solicitud
                # -------------------------------
                solicitud = Solicitud.objects.select_related(
                    "acudiente_aspirante__id_persona"
                ).get(id_solicitud=solicitud_id)

                acudiente_asp = solicitud.get_acudiente_aspirante()
                persona = acudiente_asp.get_id_persona()
                email = acudiente_asp.get_correo_electronico_aspirante()

                # -------------------------------
                # 2. Validar si la persona ya tiene usuario acudiente
                # -------------------------------
                if Usuario.objects.filter(persona=persona, role="acudiente").exists():

                    # Finalizar solicitud aunque el usuario ya exista
                    solicitud.estado_solicitud = "Finalizada"
                    solicitud.save()

                    return Response(
                        {"error": "Ya existe un usuario acudiente para esta persona"},
                        status=status.HTTP_400_BAD_REQUEST
                    )


                # -------------------------------
                # 3. Crear usuario Django
                # -------------------------------
                django_user = User.objects.create_user(
                    username=email,  # Clase Usuario se encarga de asignarlo logicamente despues, pero aqui inicializamos
                    email=email,
                    # password=str(persona.get_nit()) <--- SIN CLAVE
                )
                django_user.set_unusable_password()
                django_user.is_active = True
                django_user.save()

                # -------------------------------
                # 4. Crear usuario del sistema
                # -------------------------------
                usuario = Usuario.objects.create(
                    user=django_user,
                    persona=persona,
                    role="acudiente"
                )
                usuario.save()


                # -------------------------------
                # 5. Finalizar solicitud
                # -------------------------------
                solicitud.estado_solicitud = "Finalizada"
                solicitud.save()

                # -------------------------------
                # 6. Generación de Token y Envío de Correo
                # -------------------------------
                
                token = default_token_generator.make_token(django_user)
                uid = urlsafe_base64_encode(force_bytes(django_user.pk))
                
                link = f"https://instituto-educativo-infancia.onrender.com/restablecer_contraseña/ingresar_nueva_contraseña/ingresar_nueva_contraseña.html?token={token}&uid={uid}"
                
                asunto = "Bienvenido al Sistema - Instituto Educativo Infancia"
                mensaje = f"""
                Hola {persona.get_primer_nombre()} {persona.get_primer_apellido()},
                
                Su solicitud ha sido aprobada y su cuenta de Acudiente ha sido creada.
                
                Su código de usuario es: {usuario.get_codigo_usuario()}
                
                IMPORTANTE: Para activar su cuenta, haga clic en el siguiente enlace y configure su contraseña:
                
                {link}
                
                Este enlace expirará pronto.
                """
                
                remitente = settings.CREDENTIAL_EMAIL_HOST_USER
                
                send_mail(
                    asunto,
                    mensaje,
                    remitente,
                    [email],
                    fail_silently=False, 
                    auth_user=settings.CREDENTIAL_EMAIL_HOST_USER,
                    auth_password=settings.CREDENTIAL_EMAIL_HOST_PASSWORD
                )


                return Response(
                    {"message": "Usuario acudiente creado y credenciales enviadas"},
                    status=status.HTTP_201_CREATED
                )
            
                

        except Solicitud.DoesNotExist:
            return Response(
                {"error": "La solicitud no existe"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
             # Atomic rollback happened
            print(f"Error en crear_usuario_acudiente: {e}") # Debug log
            return Response(
                {"error": "Ha ocurrido un error... intente más tarde"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
