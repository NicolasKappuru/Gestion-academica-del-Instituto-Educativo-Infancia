from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from apps.solicitudes.models.solicitud import Solicitud
from ..models import Citacion

class ListarSolicitudesPendientesView(APIView):
    """
    Lista las solicitudes de admisión con estado 'Pendiente'.
    """
    def get(self, request):
        try:
            solicitudes = Solicitud.objects.filter(estado_solicitud='Pendiente')
            data = []
            
            for sol in solicitudes:
                acu_asp = sol.get_acudiente_aspirante()
                inf_asp = sol.get_infante_aspirante()
                
                nombre_acudiente = f"{acu_asp.get_id_persona().get_primer_nombre()} {acu_asp.get_id_persona().get_primer_apellido()}"
                nombre_aspirante = f"{inf_asp.get_id_persona().get_primer_nombre()} {inf_asp.get_id_persona().get_primer_apellido()}"
                
                data.append({
                    'id_solicitud': sol.get_id_solicitud(),
                    'nombre_acudiente': nombre_acudiente,
                    'nombre_aspirante': nombre_aspirante,
                    'correo_acudiente': acu_asp.get_correo_electronico_aspirante(),
                    'fecha_solicitud': sol.get_fecha_solicitud()
                })
            
            return Response(data)
        except Exception as e:
            return Response({'error': 'Error de conexión con la base de datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnviarCitacionEntrevistaView(APIView):
    """
    Envía una citación de entrevista para una solicitud de admisión específica.
    """
    def post(self, request):
        data = request.data
        id_solicitud = data.get('id_solicitud')
        fecha = data.get('fecha')
        hora = data.get('hora')
        lugar = data.get('lugar')
        comentario = data.get('comentario', '')
        
        if not id_solicitud or not fecha or not hora or not lugar:
            return Response({'error': 'Faltan datos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            solicitud = Solicitud.objects.get(id_solicitud=id_solicitud)
            acu_asp = solicitud.get_acudiente_aspirante()
            inf_asp = solicitud.get_infante_aspirante()
            
            correo_destinatario = acu_asp.get_correo_electronico_aspirante()

            # Validate email before everything
            validate_email(correo_destinatario)

            # Instantiate Citacion (Transient) 
            citacion = Citacion(
                nombre_acudiente=f"{acu_asp.get_id_persona().get_primer_nombre()} {acu_asp.get_id_persona().get_primer_apellido()}",
                apellido_acudiente="",
                correo_acudiente=correo_destinatario,
                nombre_acudido=f"{inf_asp.get_id_persona().get_primer_nombre()} {inf_asp.get_id_persona().get_primer_apellido()}",
                apellido_acudido="",
                fecha_cita=fecha,
                hora_cita=hora,
                lugar_cita=lugar,
                tipo_cita="Entrevista",
                motivo=f"Entrevista de admisión. {comentario}"
            )
            
            # Send Email using getters
            subject = "Citación a Entrevista de Admisión"
            message = f"""
            Estimado/a {citacion.get_nombre_acudiente()},
            
            Se ha agendado su entrevista de admisión.
            
            Fecha: {citacion.get_fecha_cita()}
            Hora: {citacion.get_hora_cita()}
            Lugar: {citacion.get_lugar_cita()}
            
            Comentarios: {comentario}
            
            Atentamente,
            Instituto Educativo Infancia
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [citacion.get_correo_acudiente()],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error enviando correo (send_mail): {e}")
                return Response({'error': 'No se ha podido enviar el correo, intente mas tarde'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Update Solicitud Status using setter - ONLY executes if send_mail succeeded
            solicitud.set_estado_solicitud('Agendado')
            solicitud.save()
            
            return Response({'message': 'Citación de entrevista enviada exitosamente'}, status=status.HTTP_200_OK)
            
        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            print(f"Error de validación de correo: {e}")
            return Response({'error': 'No se ha podido enviar el correo, intente mas tarde'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Fallback for unexpected DB or code errors
            print(f"Error general en EnviarCitacionEntrevistaView: {e}")
            return Response({'error': 'Error de conexión con la base de datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
