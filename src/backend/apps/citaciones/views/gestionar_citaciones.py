from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from apps.academico.models.grupo import Grupo
import smtplib
from apps.usuarios.models.estudiante import Estudiante
from ..models import Citacion


class ListarGruposView(APIView):
    """
    Lista todos los grupos disponibles.
    """
    def get(self, request):
        grupos = Grupo.objects.all()
        data = []
        for g in grupos:
            data.append({
                'id_grupo': g.get_id_grupo(),
                'nombre_grupo': g.get_nombre_grupo()
            })
        return Response(data)


class ListarEstudiantesGrupoView(APIView):
    """
    Lista los estudiantes de un grupo específico junto con la información de sus acudientes.
    """
    def get(self, request, id_grupo):
        try:
            grupo = Grupo.objects.get(id_grupo=id_grupo)
            estudiantes = Estudiante.objects.filter(grupo=grupo)
            data = []
            
            for est in estudiantes:
                est_persona = est.get_id_persona()
                nombre_estudiante = f"{est_persona.get_primer_nombre()} {est_persona.get_primer_apellido()}"
                
                acudiente = est.get_acudiente()
                if acudiente:
                    acu_persona = acudiente.get_id_persona()
                    nombre_acudiente = f"{acu_persona.get_primer_nombre()} {acu_persona.get_primer_apellido()}"
                    
                    # Get email from Usuario associated with Persona (Strictly per Diagram)
                    # Try to find user with 'acudiente' role first
                    usuario = acu_persona.usuarios.filter(role='acudiente').first()
                    
                    # If not found, try any user linked to the persona
                    if not usuario:
                        usuario = acu_persona.usuarios.first()

                    correo_acudiente = usuario.get_user().email if usuario and usuario.get_user() else ""

                    if correo_acudiente:
                        data.append({
                            'id_estudiante': est_persona.get_id_persona(),
                            'nombre_estudiante': nombre_estudiante,
                            'id_acudiente': acu_persona.get_id_persona(),
                            'nombre_acudiente': nombre_acudiente,
                            'correo_acudiente': correo_acudiente
                        })
            
            return Response(data)
        except Grupo.DoesNotExist:
            return Response({'error': 'Grupo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Error de conexión con la base de datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GestionarCitacionesView(APIView):
    """
    Envía citaciones por correo electrónico a los acudientes seleccionados de forma atómica.
    """
    def post(self, request):
        data = request.data
        citaciones_list = data.get('citaciones', [])
        fecha = data.get('fecha')
        hora = data.get('hora')
        lugar = data.get('lugar')
        motivo = data.get('motivo')
        
        if not citaciones_list or not fecha or not hora or not lugar or not motivo:
            return Response({'error': 'Faltan datos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        # First pass: Validate all data and prepare messages
        messages = []
        
        try:
            for item in citaciones_list:
                correo = item.get('correo_acudiente', '')
                nombre_acudiente = item.get('nombre_acudiente', 'Acudiente')

                if not correo:
                    print(f"Error: Correo faltante para {nombre_acudiente}")
                    return Response({'error': 'No se ha podido enviar los correos, intente mas tarde'}, status=status.HTTP_400_BAD_REQUEST)

                # Validate email format
                validate_email(correo)

                # Validate domain existence (Removed simple DNS check in favor of global SMTP check)
                # We will collect all emails and verify them in bulk at the end of the loop before sending.
                # However, to keep structure clean, we can just collect them here.
                
                # Check duplication - if needed, but 'send_mass_mail' handles lists.
                # Just proceed to object creation.

                # Instantiate Citacion (Transient) to use its helpers/getters
                citacion = Citacion(
                    nombre_acudiente=nombre_acudiente,
                    apellido_acudiente="",
                    correo_acudiente=correo,
                    nombre_acudido=item.get('nombre_estudiante', ''),
                    apellido_acudido="",
                    fecha_cita=fecha,
                    hora_cita=hora,
                    lugar_cita=lugar,
                    tipo_cita="General",
                    motivo=motivo
                )
                
                # Construct email components
                subject = f"Citación: {citacion.get_motivo()}"
                message_body = f"""
                Estimado acudiente {citacion.get_nombre_acudiente()},
                
                Se le cita para el asunto: {citacion.get_motivo()}.
                
                Fecha: {citacion.get_fecha_cita()}
                Hora: {citacion.get_hora_cita()}
                Lugar: {citacion.get_lugar_cita()}
                
                Atentamente,
                Instituto Educativo Infancia
                """
                
                # Add to batch list: (subject, message, sender, [recipient])
                messages.append((
                    subject,
                    message_body,
                    settings.EMAIL_HOST_USER,
                    [citacion.get_correo_acudiente()]
                ))

            # Atomic Pre-Check: Verify all recipients with the SMTP server before sending anything.
            if messages:
                # Extract all unique recipients to verify
                all_recipients = set()
                for m in messages:
                    # m[3] is the recipient list
                    for r in m[3]:
                        all_recipients.add(r)
                
                try:
                    # Connect to SMTP server
                    connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    # connection.set_debuglevel(1) # Debug if needed
                    if settings.EMAIL_USE_TLS:
                        connection.starttls()
                    
                    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                        connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    
                    # Start transaction to verify address
                    sender = settings.EMAIL_HOST_USER
                    connection.mail(sender)
                    
                    for recipient in all_recipients:
                        code, msg = connection.rcpt(recipient)
                        if code not in [250, 251]:
                            connection.quit()
                            # This is the crucial atomic failure point
                            print(f"SMTP Error verifying {recipient}: {code} - {msg}")
                            return Response({'error': 'No se ha podido enviar los correos, intente mas tarde'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    connection.quit()
                    
                except Exception as smtp_error:
                    print(f"SMTP Pre-check connection error: {smtp_error}")
                    # If we can't verify, we assume unsafe to send if we want strict atomicity? 
                    # Or we treat connection error as generic error.
                    return Response({'error': 'No se ha podido enviar los correos, intente mas tarde'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Atomic Send: If we got here, all recipients are accepted by the server.

            # Atomic Send: If we got here, all formats are valid (locally).
            # send_mass_mail opens a single connection.
            if messages:
                send_mass_mail(tuple(messages), fail_silently=False)

            return Response({'message': 'Citaciones enviadas exitosamente'}, status=status.HTTP_200_OK)

        except ValidationError as e:
            print(f"Error de validación de correo en lote: {e}")
            return Response({'error': 'No se ha podido enviar los correos, intente mas tarde'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch SMTP errors or other issues
            print(f"Error enviando correos masivos: {e}")
            return Response({'error': 'No se ha podido enviar los correos, intente mas tarde'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
