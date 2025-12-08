from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

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
                
                nombre_acudiente = f"{acu_asp.id_persona.primer_nombre} {acu_asp.id_persona.primer_apellido}"
                nombre_aspirante = f"{inf_asp.id_persona.primer_nombre} {inf_asp.id_persona.primer_apellido}"
                
                data.append({
                    'id_solicitud': sol.get_id_solicitud(),
                    'nombre_acudiente': nombre_acudiente,
                    'nombre_aspirante': nombre_aspirante,
                    'correo_acudiente': acu_asp.correo_electronico_aspirante,
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
            
            # Instantiate Citacion (Transient) 
            citacion = Citacion(
                nombre_acudiente=f"{acu_asp.id_persona.primer_nombre} {acu_asp.id_persona.primer_apellido}",
                apellido_acudiente="",
                correo_acudiente=acu_asp.correo_electronico_aspirante,
                nombre_acudido=f"{inf_asp.id_persona.primer_nombre} {inf_asp.id_persona.primer_apellido}",
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
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [citacion.get_correo_acudiente()],
                fail_silently=False,
            )
            
            # Update Solicitud Status using setter
            solicitud.set_estado_solicitud('Agendado')
            solicitud.save()
            
            return Response({'message': 'Citación de entrevista enviada exitosamente'}, status=status.HTTP_200_OK)
            
        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Check if it's likely an email error
            if 'mail' in str(e).lower() or 'smtp' in str(e).lower():
                return Response({'error': 'Error al enviar el correo'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error': 'Error de conexión con la base de datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
