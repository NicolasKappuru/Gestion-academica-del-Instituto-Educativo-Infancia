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

from apps.usuarios.models.persona import Persona
from apps.usuarios.models.usuario import Usuario

from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.profesor import Profesor
from apps.usuarios.models.administrador_academico import Administrador_academico
from apps.usuarios.models.administrador_de_usuarios import Administrador_de_usuarios


class CrearUsuario(APIView):

    def post(self, request):
        role = request.data.get("role")
        primer_nombre = request.data.get("primer_nombre")
        segundo_nombre = request.data.get("segundo_nombre")
        primer_apellido = request.data.get("primer_apellido")
        segundo_apellido = request.data.get("segundo_apellido")

        email = request.data.get("email")
        nit = request.data.get("nit")

        # Validar campos obligatorios
        if not role or not email or not nit:
            return Response(
                {"error": "Debe enviar role, email y nit"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar rol existente
        roles_validos = [r[0] for r in Usuario.ROLES]
        if role not in roles_validos:
            return Response(
                {"error": "El rol enviado no es válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Atomicidad y Manejo de Errores
            with transaction.atomic():

                # Verificar si el NIT ya tiene un usuario con el mismo rol
                persona = Persona.objects.filter(NIT=nit).first()
                    
                if persona:
                    # Ya existe una persona con ese NIT, revisar si ya tiene el rol
                    if Usuario.objects.filter(persona=persona, role=role).exists():
                        return Response(
                            {"error": "Ya existe una persona con usuario de ese rol"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    # No existe → crear persona nueva
                    persona = Persona(
                    primer_nombre=primer_nombre,
                    segundo_nombre=segundo_nombre,
                    primer_apellido=primer_apellido,
                    segundo_apellido=segundo_apellido,
                    NIT=nit
                    )
                    persona.save()


                # Crear usuario Django
                django_user = User.objects.create_user(
                    username=email, # Clase Usuario se encarga de asignarlo correctamente si es necesario un update
                    email=email,
                    # password=str(nit)  <-- NO ASIGNAR CONTRASEÑA
                )
                
                # Encapsulamiento: NO usar atributos directos si hay métodos (aunque User es standard)
                # Requerimiento: user.set_unusable_password()
                django_user.set_unusable_password()
                django_user.is_active = True
                django_user.save()

                # Crear usuario del sistema
                usuario = Usuario.objects.create(
                    user=django_user,
                    persona=persona,
                    role=role
                )
                usuario.save()

                # Crear el objeto especializado segun el rol
                if role == "profesor":
                    profesor = Profesor.objects.create(id_persona=persona)
                    profesor.save()

                elif role == "administrador_academico":
                    administrador_academico =Administrador_academico.objects.create(id_persona=persona)
                    administrador_academico.save() 

                elif role == "administrador_usuarios":
                    administrador_de_usuarios = Administrador_de_usuarios.objects.create(id_persona=persona)
                    administrador_de_usuarios.save()

                # -------------------------------
                # Generación de Token y Envío de Correo
                # -------------------------------
                
                # Generar token y uid
                token = default_token_generator.make_token(django_user)
                uid = urlsafe_base64_encode(force_bytes(django_user.pk))
                
                # Construir link (Ajustar dominio segun necesidad, aqui asumimos localhost frontend)
                # El frontend debe estar en esa ruta
                link = f"http://127.0.0.1:5500/src/frontend/restablecer_contraseña/ingresar_nueva_contraseña/ingresar_nueva_contraseña.html?token={token}&uid={uid}"
                
                role_display = role.replace("_", " ").title()
                
                asunto = "Bienvenido al Sistema de Gestión Académica"
                mensaje = f"""
                Hola {primer_nombre} {primer_apellido},
                
                Bienvenido al Instituto Educativo Infancia.
                Su cuenta ha sido creada con el rol: {role_display}.
                
                Su código de usuario es: {usuario.get_codigo_usuario()}
                
                IMPORTANTE: Para activar su cuenta, haga clic en el siguiente enlace y configure su contraseña:
                
                {link}
                
                Este enlace expirará pronto.
                """
                
                remitente = settings.CREDENTIAL_EMAIL_HOST_USER
                
                # Enviar correo (Si falla, transaction.atomic hará rollback)
                send_mail(
                    asunto,
                    mensaje,
                    remitente,
                    [email],
                    fail_silently=False, # Importante: False para que lance excepción si falla
                    auth_user=settings.CREDENTIAL_EMAIL_HOST_USER,
                    auth_password=settings.CREDENTIAL_EMAIL_HOST_PASSWORD
                )

                return Response(
                    {
                        "message": "Usuario creado y credenciales enviadas",
                        "usuario_id": usuario.get_codigo_usuario(),
                        "persona_id": persona.get_id_persona(),
                        "user_id": django_user.id
                    },
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            # Captura cualquier error (DB o Email)
            # Como salimos del bloque atomic con excepcion, el rollback ya ocurrió automatico
            print(f"Error en crear_usuario: {e}") # Debug log
            return Response(
                {"error": "Ha ocurrido un error... intente más tarde"}, # Mensaje generico solicitado
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
