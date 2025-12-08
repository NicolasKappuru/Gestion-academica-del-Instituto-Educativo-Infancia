from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from apps.academico.models.grupo import Grupo
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
                nombre_estudiante = f"{est_persona.primer_nombre} {est_persona.primer_apellido}"
                
                acudiente = est.get_acudiente()
                if acudiente:
                    acu_persona = acudiente.get_id_persona()
                    nombre_acudiente = f"{acu_persona.primer_nombre} {acu_persona.primer_apellido}"
                    
                    # Get email from Usuario associated with Persona (Strictly per Diagram)
                    # Try to find user with 'acudiente' role first
                    usuario = acu_persona.usuarios.filter(role='acudiente').first()
                    
                    # If not found, try any user linked to the persona
                    if not usuario:
                        usuario = acu_persona.usuarios.first()

                    correo_acudiente = usuario.user.email if usuario and usuario.user else ""

                    data.append({
                        'id_estudiante': est_persona.id_persona,
                        'nombre_estudiante': nombre_estudiante,
                        'id_acudiente': acu_persona.id_persona,
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
    Envía citaciones por correo electrónico a los acudientes seleccionados.
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

        missing_emails = []
        failed_emails = []

        # No DB transaction needed for Citacion as it is transient
        for item in citaciones_list:
            
            correo = item.get('correo_acudiente', '')
            nombre_acudiente = item.get('nombre_acudiente', 'Acudiente')

            if not correo:
                missing_emails.append(nombre_acudiente)
                continue 

            # Instantiate Citacion (Transient) using setters
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
            
            # Send Email using getters
            subject = f"Citación: {citacion.get_motivo()}"
            message = f"""
            Estimado acudiente {citacion.get_nombre_acudiente()},
            
            Se le cita para el asunto: {citacion.get_motivo()}.
            
            Fecha: {citacion.get_fecha_cita()}
            Hora: {citacion.get_hora_cita()}
            Lugar: {citacion.get_lugar_cita()}
            
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
                print(f"Error sending mail to {correo}: {e}") # Log error
                failed_emails.append(citacion.get_correo_acudiente())
        
        # Build response message
        response_data = {}
        status_code = status.HTTP_200_OK

        if failed_emails or missing_emails:
            status_code = status.HTTP_207_MULTI_STATUS
            response_data['message'] = 'Proceso completado con advertencias'
            response_data['details'] = {
                'failed_emails': failed_emails,
                'missing_emails_users': missing_emails
            }
        else:
            response_data['message'] = 'Citaciones enviadas exitosamente'

        if len(failed_emails) + len(missing_emails) == len(citaciones_list) and len(citaciones_list) > 0:
             return Response({
                'error': 'No se pudo enviar ninguna citación válida', 
                'details': response_data.get('details')
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status_code)
        
        return Response({'message': 'Citaciones enviadas exitosamente'}, status=status.HTTP_200_OK)
