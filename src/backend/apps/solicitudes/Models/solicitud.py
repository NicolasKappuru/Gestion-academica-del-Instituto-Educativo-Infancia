from django.db import models
from apps.usuarios.models.acudiente_aspirante import Acudiente_aspirante
from apps.usuarios.models.infante_aspirante import Infante_aspirante

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)

    acudiente_aspirante = models.ForeignKey(
    Acudiente_aspirante,
    on_delete=models.CASCADE,
    db_column='id_acudiente_aspirante'
    )

    infante_aspirante = models.ForeignKey(
        Infante_aspirante,
        on_delete=models.CASCADE,
        db_column='id_infante_aspirante'
    )

    grado_aplicar = models.CharField(max_length=15, null=False, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=15, default='Pendiente')

    class Meta:
        db_table = 'Solicitud'

    #GETTERS
    
    def get_id_solicitud(self):
        return self.id_solicitud

    def get_acudiente_aspirante(self):
        return self.acudiente_aspirante

    def get_infante_aspirante(self):
        return self.infante_aspirante

    def get_grado_aplicar(self):
        return self.grado_aplicar

    def get_fecha_solicitud(self):
        return self.fecha_solicitud

    def get_estado_solicitud(self):
        return self.estado_solicitud

    #SETTERS
    
    def set_acudiente_aspirante(self, value):
        self.acudiente_aspirante = value

    def set_infante_aspirante(self, value):
        self.infante_aspirante = value

    def set_grado_aplicar(self, value):
        self.grado_aplicar = value

    def set_estado_solicitud(self, value):
        self.estado_solicitud = value
