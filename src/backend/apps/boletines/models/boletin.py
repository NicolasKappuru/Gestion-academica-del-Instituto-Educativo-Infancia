from django.db import models
from apps.academico.models.periodo_academico import Periodo_academico

class Boletin(models.Model):
    id_boletin = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=30) 
    profesor_director = models.CharField(max_length=250)

    estudiante = models.ForeignKey(
        "usuarios.Estudiante",
        db_column='id_persona_estudiante',
        related_name='boletines',
        null=True,
        on_delete=models.SET_NULL
    )

    periodo_academico = models.ForeignKey(
        Periodo_academico, 
        db_column="anio",
        on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'Boletin'

    #GETTERS

    def get_id_boletin(self):
        return self.id_boletin

    def get_nombre_grupo(self):
        return self.nombre_grupo

    def get_profesor_director(self):
        return self.profesor_director

    def get_estudiante(self):
        return self.estudiante

    def get_periodo_academico(self):
        return self.periodo_academico

    #SETTERS
    
    def set_nombre_grupo(self, value):
        self.nombre_grupo = value

    def set_profesor_director(self, value):
        self.profesor_director = value

    def set_estudiante(self, value):
        self.estudiante = value

    def set_periodo_academico(self, value):
        self.periodo_academico = value
