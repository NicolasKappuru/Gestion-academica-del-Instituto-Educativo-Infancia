#Para ejecutar el scrip
#python manage.py cargar_datos

from django.core.management.base import BaseCommand
from datetime import date
from apps.academico.models.periodo_academico import Periodo_academico
from apps.academico.models.grado import Grado
from apps.academico.models.grupo import Grupo
from apps.academico.models.categoria_logros import Categoria_logros
from apps.academico.models.logro import Logro


class Command(BaseCommand):  
    help = "Carga categorías, grados, grupos y logros iniciales."

    def handle(self, *args, **kwargs):

        # --------------------
        # PERIODO ACADÉMICO
        # --------------------
        periodo_2025, _ = Periodo_academico.objects.get_or_create(
            anio=2025,
            defaults={
                "fecha_inicio": date(2025, 2, 1),
                "fecha_fin": date(2025, 10, 31),
            },
        )

        # --------------------
        # CATEGORÍAS
        # --------------------
        categorias_info = {
            "Desarrollo físico": "Favorece el movimiento, coordinación y habilidades motrices básicas.",
            "Lenguaje y comunicación": "Permite expresar ideas, necesidades y comprender al entorno.",
            "Desarrollo cognitivo": "Estimula el pensamiento, la lógica y la resolución de problemas.",
            "Desarrollo social y emocional": "Fortalece relaciones, convivencia y reconocimiento emocional.",
            "Autocuidado y vida diaria": "Desarrolla independencia en rutinas personales y escolares.",
            "Comprensión del entorno y exploración": "Promueve curiosidad y comprensión del espacio y objetos.",
            "Salud y nutrición": "Fomenta hábitos saludables y autocuidado físico.",
        }

        categorias = {}
        for nombre, desc in categorias_info.items():
            cat, _ = Categoria_logros.objects.get_or_create(
                nombre_categoria=nombre,
                defaults={"descripcion_categoria": desc},
            )
            categorias[nombre] = cat

        # --------------------
        # GRADOS
        # --------------------
        grados_nombres = ["Párvulos", "Caminadores", "Prejardín"]
        grados = {}

        for g in grados_nombres:
            grado, _ = Grado.objects.get_or_create(
                nombre_grado=g,
                periodo_acadmico=periodo_2025,
                defaults={"cupos_grado": 20},
            )
            grados[g] = grado

        # --------------------
        # GRUPOS
        # --------------------
        for nombre, grado in grados.items():
            for i in range(1, 3):
                Grupo.objects.get_or_create(
                    nombre_grupo=f"{nombre}{i}{periodo_2025.anio}",
                    grado=grado,                    
                )

        # --------------------
        # LOGROS
        # --------------------
        logros_data = {
            "Desarrollo físico": {
                "Caminadores": [
                    "Camina con seguridad por el aula.",
                    "Sube y baja pequeños escalones con apoyo.",
                    "Manipula objetos grandes con ambas manos.",
                ],
                "Párvulos": [
                    "Corre y se detiene sin perder equilibrio.",
                    "Atrapa una pelota grande con ambas manos.",
                    "Ensarta piezas o mete objetos en recipientes con precisión.",
                ],
                "Prejardín": [
                    "Salta con ambos pies juntos.",
                    "Realiza trazos circulares y líneas con intención.",
                    "Usa tijeras de punta redonda con ayuda.",
                ],
            },

            "Lenguaje y comunicación": {
                "Caminadores": [
                    "Señala objetos cuando se le nombran.",
                    "Produce palabras para pedir o expresar necesidades básicas.",
                    "Imita sonidos y gestos del adulto.",
                ],
                "Párvulos": [
                    "Forma frases simples de 2–3 palabras.",
                    "Describe brevemente lo que está viendo o haciendo.",
                    "Sigue instrucciones de un solo paso.",
                ],
                "Prejardín": [
                    "Mantiene pequeñas conversaciones con sus pares o el adulto.",
                    "Usa pronombres y vocabulario variado.",
                    "Comprende y sigue instrucciones de dos pasos.",
                ],
            },

            "Desarrollo cognitivo": {
                "Caminadores": [
                    "Explora objetos para descubrir cómo funcionan.",
                    "Clasifica objetos simples (grande/pequeño).",
                    "Imita acciones del adulto durante el juego.",
                ],
                "Párvulos": [
                    "Clasifica por color o forma básica.",
                    "Resuelve problemas sencillos como encajar piezas.",
                    "Participa en juego simbólico simple.",
                ],
                "Prejardín": [
                    "Ordena objetos por tamaño o secuencias simples.",
                    "Anticipa resultados de acciones.",
                    "Realiza juego simbólico con roles.",
                ],
            },

            "Desarrollo social y emocional": {
                "Caminadores": [
                    "Juega al lado de otros niños.",
                    "Reconoce y busca a adultos de confianza.",
                    "Expresa emociones básicas con gestos y palabras.",
                ],
                "Párvulos": [
                    "Comparte materiales con apoyo.",
                    "Inicia interacciones cortas con otros niños.",
                    "Muestra capacidad inicial para esperar turnos.",
                ],
                "Prejardín": [
                    "Participa en juegos cooperativos simples.",
                    "Identifica emociones propias y ajenas.",
                    "Sigue normas básicas del aula sin recordatorio constante.",
                ],
            },

            "Autocuidado y vida diaria": {
                "Caminadores": [
                    "Intenta comer solo usando manos o cuchara.",
                    "Colabora en ponerse prendas sencillas.",
                    "Indica cuando necesita cambio de pañal o apoyo.",
                ],
                "Párvulos": [
                    "Usa cuchara o vaso con poca ayuda.",
                    "Se lava las manos con asistencia.",
                    "Colabora en recoger sus materiales.",
                ],
                "Prejardín": [
                    "Se viste parcialmente solo.",
                    "Sigue rutinas de higiene con mínima ayuda.",
                    "Mantiene orden en su espacio de trabajo.",
                ],
            },

            "Comprensión del entorno y exploración": {
                "Caminadores": [
                    "Reconoce objetos y lugares del jardín.",
                    "Explora rincones y materiales con curiosidad.",
                    "Identifica miembros del grupo y adultos principales.",
                ],
                "Párvulos": [
                    "Identifica partes del cuerpo.",
                    "Participa en exploración sensorial.",
                    "Ubica objetos en espacios conocidos.",
                ],
                "Prejardín": [
                    "Comprende conceptos espaciales básicos.",
                    "Identifica características del entorno.",
                    "Observa fenómenos simples y comenta sobre ellos.",
                ],
            },

            "Salud y nutrición": {
                "Caminadores": [
                    "Muestra apetito estable y participa en las comidas.",
                    "Presenta crecimiento adecuado a su edad.",
                ],
                "Párvulos": [
                    "Acepta variedad de alimentos según orientación.",
                    "Colabora en rutinas de cuidado físico.",
                ],
                "Prejardín": [
                    "Reconoce hábitos saludables básicos.",
                    "Tiene autonomía básica en su alimentación diaria.",
                ],
            },
        }

        total = 0

        for categoria, grados_dict in logros_data.items():
            categoria_obj = categorias[categoria]

            for grado, lista_logros in grados_dict.items():
                grado_obj = grados[grado]

                for texto in lista_logros:
                    Logro.objects.get_or_create(
                        concepto_logro=texto[:50],
                        grado=grado_obj,
                        categoria_logros=categoria_obj,
                        defaults={"descripcion_logro": texto},
                    )
                    total += 1
    
        self.stdout.write(self.style.SUCCESS("Carga inicial completada."))
