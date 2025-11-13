from django.db import models
from apps.usuarios.models.acudiente_aspirante import Acudiente_aspirante
from apps.usuarios.models.infante_aspirante import Infante_aspirante

class Solicitud(models.Model):
    acudiente_aspirante = models.OneToOneField(
        Acudiente_aspirante,
        on_delete=models.CASCADE,
        related_name='solicitud'
    )
    infante_aspirante = models.OneToOneField(
        Infante_aspirante,
        on_delete=models.CASCADE,
        related_name='solicitud'
    )
    
    grado_aplicar = models.CharField(max_length=15, null=False, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Solicitud de {self.acudiente_aspirante.persona.primer_nombre} - {self.estado}"
