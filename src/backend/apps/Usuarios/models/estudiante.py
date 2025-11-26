from django.db import models
from .persona import Persona
from .acudiente import Acudiente
from apps.academico.models.grupo import Grupo

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
        related_name='estudiantes', 
        db_column='id_persona_acudiente'
    )

    grupo = models.ForeignKey(
        Grupo,     
        on_delete=models.SET_NULL,
        null=True,
        related_name='estudiantes',
        db_column='id_grupo'
    )

    class Meta:
        db_table = 'Estudiante'

    #GETTERS
    def get_id_persona(self):
        return self.id_persona

    def get_fecha_nacimiento(self):
        return self.fecha_nacimiento

    def get_acudiente(self):
        return self.acudiente

    def get_grupo(self):
        return self.grupo

    #SETTERS
    
    def set_fecha_nacimiento(self, value):
        self.fecha_nacimiento = value

    def set_acudiente(self, value):
        self.acudiente = value

    def set_grupo(self, value):
        self.grupo = value
