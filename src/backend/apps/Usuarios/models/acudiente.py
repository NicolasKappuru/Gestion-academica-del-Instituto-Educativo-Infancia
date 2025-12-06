from django.db import models
from .persona import Persona


class Acudiente(models.Model):
    id_persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persona',
    )

    class Meta:
        db_table = 'Acudiente'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estudiantes_acudidos = [] 

    def consultar_lista(self):
        self.estudiantes_acudidos = list(self.estudiantes.all())

    def agregar_estudiante(self, acudido):
        acudido.set_acudiente(self)
        acudido.save()
        self.estudiantes_acudidos.append(acudido)
        return True

    def eliminar_estudiante(self, id_estudiante: int):
        estudiante = Estudiante.objects.get(pk=id_estudiante, acudiente=self)
        estudiante.acudiente = None
        estudiante.save()
        self.estudiantes = [
            e for e in self.estudiantes_acudidos if e.get_id_persona() != id_estudiante
        ]

        return True

    #GETTERS
    def get_id_persona(self):
        return self.id_persona
    
    #SETTERS
    def set_id_persona(self, value):
        self.id_persona = value 