from django.db import models
from .persona import Persona

class Administrador_academico(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
    )

    class Meta:
        db_table = 'Administrador_academico'

    #GETTERS

    def get_id_persona(self):
        return self.id_persona
