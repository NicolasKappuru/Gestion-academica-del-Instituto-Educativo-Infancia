# apps/usuarios/models/estudiante.py
from django.db import models
from .persona import Persona
from .acudiente import Acudiente
from apps.adacemico.models.grupo import Grupo

class Estudiante(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
    )
    
    fecha_nacimiento = models.DateField()
    
    acudiente = models.ForeignKey(
        Acudiente,
        on_delete=models.SET_NULL,  
        null=True,
        related_name='estudiantes'  
    )

    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.SET_NULL,
        null=True,
        related_name='estudiantes'
    )
    
    class Meta:
        db_table = 'Estudiante'
