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

    #GETTERS

    def get_id_persona(self):
        return self.id_persona

    def get_primer_nombre(self):
        return self.primer_nombre

    def get_segundo_nombre(self):
        return self.segundo_nombre

    def get_primer_apellido(self):
        return self.primer_apellido

    def get_segundo_apellido(self):
        return self.segundo_apellido

    def get_nit(self):
        return self.NIT

    #SETTERS

    def set_id_persona(self, value):
        self.id_persona = value 
    
    def set_primer_nombre(self, value):
        self.primer_nombre = value

    def set_segundo_nombre(self, value):
        self.segundo_nombre = value

    def set_primer_apellido(self, value):
        self.primer_apellido = value

    def set_segundo_apellido(self, value):
        self.segundo_apellido = value

    def set_nit(self, value):
        self.NIT = value

