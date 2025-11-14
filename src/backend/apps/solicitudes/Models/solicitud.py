from django.db import models
from apps.usuarios.models.acudiente_aspirante import Acudiente_aspirante
from apps.usuarios.models.infante_aspirante import Infante_aspirante

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)

    acudiente_aspirante = models.OneToOneField(
        Acudiente_aspirante,
        on_delete=models.CASCADE,
        db_column='id_acudiente_aspirante'
    )

    infante_aspirante = models.OneToOneField(
        Infante_aspirante,
        on_delete=models.CASCADE,
        db_column='id_infante_aspirante'
    )
    
    grado_aplicar = models.CharField(max_length=15, null=False, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=15, default='Pendiente')

    class Meta:
        db_table = 'Solicitud'

    def __str__(self):
        return f"Solicitud de {self.acudiente_aspirante.id_persona.primer_nombre} - {self.estado_solicitud}"
