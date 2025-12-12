from django.db import models
from .persona import Persona

class Acudiente_aspirante(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',  
    )
    correo_electronico_aspirante = models.EmailField()

    class Meta:
            db_table = 'Acudiente_aspirante'

    #GETTERS

    def get_id_persona(self):
        return self.id_persona
    
    def get_correo_electronico_aspirante(self):
        return self.correo_electronico_aspirante
    
    #SETTERS

    def set_correo_electronico_aspirante(self, value):
        self.correo_electronico_aspirante = value