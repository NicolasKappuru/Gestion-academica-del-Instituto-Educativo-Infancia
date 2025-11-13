from django.urls import path
from .views.form_inscripcion_view import FormularioInscripcion

urlpatterns = [
    path('formularioInscripcion/', FormularioInscripcion.as_view(), name='formularioInscripcion'),
]
