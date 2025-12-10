from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.usuarios.models.persona import Persona
from apps.usuarios.models.acudiente_aspirante import Acudiente_aspirante
from apps.usuarios.models.infante_aspirante import Infante_aspirante
from apps.solicitudes.models.solicitud import Solicitud

@method_decorator(csrf_exempt, name='dispatch')
class FormularioInscripcion(APIView):
    def post(self, request):
        
        priNomAcu = request.data.get("primerNombreAcudiente")
        segNomAcu = request.data.get("segundoNombreAcudiente")
        priApeAcu = request.data.get("primerApellidoAcudiente")
        segApeAcu = request.data.get("segundoApellidoAcudiente")
        correoAcu = request.data.get("correoAcudiente")
        cedulaAcu = request.data.get("cedulaAcudiente")

        priNomInf = request.data.get("primerNombreInfante")
        segNomInf = request.data.get("segundoNombreInfante")
        priApeInf = request.data.get("primerApellidoInfante")
        segApeInf = request.data.get("segundoApellidoInfante")
        fechaInf = request.data.get("fechaInfante")

        grado = request.data.get("grado_aplicado")
        
        personaAcu = Persona.objects.filter(NIT=cedulaAcu).first()

        if not personaAcu:
            personaAcu = Persona(
                primer_nombre=priNomAcu,
                segundo_nombre=segNomAcu,
                primer_apellido=priApeAcu,
                segundo_apellido=segApeAcu,
                NIT=cedulaAcu
            )
    
        personaInf = Persona(
            primer_nombre = priNomInf,
            segundo_nombre = segNomInf,
            primer_apellido = priApeInf,
            segundo_apellido = segApeInf,
            NIT = None
        )

        acudienteAspirante = Acudiente_aspirante.objects.filter(id_persona=personaAcu).first()

        if not acudienteAspirante:
            acudienteAspirante = Acudiente_aspirante(
                id_persona=personaAcu,
                correo_electronico_aspirante=correoAcu
            )


        infanteAspirante = Infante_aspirante(
            id_persona = personaInf,
            fecha_nacimiento = fechaInf
        )

        solicitud = Solicitud(
            acudiente_aspirante = acudienteAspirante,
            infante_aspirante = infanteAspirante,
            grado_aplicar = grado,
         )    
    
        try:
            # Guardar los objetos en la BD
            personaAcu.save()
            personaInf.save()
            acudienteAspirante.save()
            infanteAspirante.save()
            solicitud.save()
            
            return Response({
                "message": "Preinscripción registrada correctamente"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si algo falla, devuelves error
            return Response({
                "error": f"Error al guardar los datos: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
