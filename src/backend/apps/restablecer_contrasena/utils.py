from django.core.mail import get_connection, EmailMessage
from django.conf import settings

def enviar_correo_restablecimiento(usuario, enlace):
    """
    Envía el correo de restablecimiento usando una conexión SMTP específica.
    """
    try:
        # Configuración específica para este módulo
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.PASSWORD_RESET_EMAIL_HOST_USER,
            password=settings.PASSWORD_RESET_EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        )

        subject = 'Restablecimiento de Contraseña'
        body = f'Hola {usuario.user.first_name},\n\n' \
               f'Has solicitado restablecer tu contraseña. Ingresa al siguiente enlace para continuar:\n\n' \
               f'{enlace}\n\n' \
               f'Si no solicitaste esto, ignora este mensaje.'
        
        email = EmailMessage(
            subject,
            body,
            settings.PASSWORD_RESET_EMAIL_HOST_USER,
            [usuario.user.email],
            connection=connection
        )
        
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False
