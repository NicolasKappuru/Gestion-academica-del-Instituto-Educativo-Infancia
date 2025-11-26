from django.db import models
from .grado import Grado
from apps.usuarios.models.profesor import Profesor

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=25) 
    cupos_grupo = models.DecimalField(max_digits=2, decimal_places=0, default=10)

    grado = models.ForeignKey(
        Grado,
        db_column='id_grado',
        on_delete=models.CASCADE,
        null=True

    )

    profesor_director = models.ForeignKey(
        Profesor, 
        db_column="id_persona_profesor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'Grupo'

    def asignar_estudiante(self, estudiante):
        if self.estudiantes.count() >= self.cupos_grupo:
            raise ValueError("No hay cupos disponibles en este grupo")
        
        estudiante.grupo = self
        estudiante.save()


    #GETTERS
    
    def get_id_grupo(self):
        return self.id_grupo

    def get_nombre_grupo(self):
        return self.nombre_grupo

    def get_cupos_grupo(self):
        return self.cupos_grupo

    def get_grado(self):
        return self.grado

    def get_profesor_director(self):
        return self.profesor_director

    # ===========================
    #          SETTERS
    # ===========================
    def set_nombre_grupo(self, value):
        self.nombre_grupo = value

    def set_cupos_grupo(self, value):
        self.cupos_grupo = value

    def set_grado(self, value):
        self.grado = value

    def set_profesor_director(self, value):
        self.profesor_director = value
