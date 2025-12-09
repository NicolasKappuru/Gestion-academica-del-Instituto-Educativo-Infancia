from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction

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
                    username=email, # Clase Usuario se encarga de asignarlo
                    email=email,
                    password=str(nit)
                )
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

                return Response(
                    {
                        "message": "Usuario creado correctamente",
                        "usuario_id": usuario.get_codigo_usuario(),
                        "persona_id": persona.get_id_persona(),
                        "user_id": django_user.id
                    },
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
