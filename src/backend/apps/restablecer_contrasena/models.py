from django.db import models
from django.utils import timezone
from apps.usuarios.models.usuario import Usuario

class IntentoRestablecimiento(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='intento_restablecimiento')
    intentos_datos = models.IntegerField(default=0)
    intentos_contrasena = models.IntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)
    
    # Token temporal para validar que el usuario viene del correo
    token_validacion = models.CharField(max_length=100, null=True, blank=True)
    fecha_token = models.DateTimeField(null=True, blank=True)

    def esta_bloqueado(self):
        if self.bloqueado_hasta and timezone.now() < self.bloqueado_hasta:
            return True
        return False

    def reiniciar_intentos_datos(self):
        self.intentos_datos = 0
        self.bloqueado_hasta = None
        self.save()

    def reiniciar_intentos_contrasena(self):
        self.intentos_contrasena = 0
        self.save()

    def registrar_fallo_datos(self):
        self.intentos_datos += 1
        if self.intentos_datos > 3:
            self.bloqueado_hasta = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

    def registrar_fallo_contrasena(self):
        self.intentos_contrasena += 1
        self.save()
