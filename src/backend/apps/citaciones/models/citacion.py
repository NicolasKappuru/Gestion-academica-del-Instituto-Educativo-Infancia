from django.db import models
from apps.usuarios.models.acudiente import Acudiente
from apps.usuarios.models.administrador_academico import Administrador_academico


class Citacion(models.Model):
    id_citacion = models.AutoField(
        primary_key=True,
        db_column='id_citacion'
    )

    fecha_cita = models.DateField(
        db_column='fecha_cita'
    )

    lugar_cita = models.CharField(
        max_length=50,
        db_column='lugar_cita'
    )

    hora_cita = models.TimeField(
        db_column='hora_cita'
    )

    tipo_cita = models.CharField(
        max_length=15,
        db_column='tipo_cita'
    )

    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_persona_acudiente',
    )

    administrador = models.ForeignKey(
        Administrador_academico,
        on_delete=models.SET_NULL,
        null=True,
        db_column='id_persona_administrador_academico',
    )
    
    class Meta:
        db_table = 'Citacion'
