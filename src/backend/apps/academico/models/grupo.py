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
