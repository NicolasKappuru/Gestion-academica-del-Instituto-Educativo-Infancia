from django.db import models

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    NIT = models.DecimalField(max_digits=10, decimal_places=0, null=True, unique=True)

    class Meta:
        db_table = 'Persona'
        abstract = False

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"
    
   