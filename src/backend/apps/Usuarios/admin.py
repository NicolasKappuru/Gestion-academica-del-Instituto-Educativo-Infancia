from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Acudiente)
admin.site.register(Profesor)
admin.site.register(AdministradorAcademico)
admin.site.register(AdministradorDeUsuarios)
