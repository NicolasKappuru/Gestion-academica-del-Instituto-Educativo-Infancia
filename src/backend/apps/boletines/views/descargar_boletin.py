# apps/boletines/views/descargar_boletin.py
import io
from collections import defaultdict

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

from apps.boletines.models.boletin import Boletin
from apps.usuarios.models.estudiante import Estudiante
from apps.academico.models.evaluacion import Evaluacion


class DescargarBoletin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
   
        id_boletin = request.data.get("id_boletin")
        id_persona = request.data.get("id_persona")

        if not id_boletin:
            return HttpResponse(
                b"Falta id_boletin",
                status=status.HTTP_400_BAD_REQUEST
            )

        if not id_persona:
            return HttpResponse(
                b"Falta id_persona (id del estudiante)",
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            boletin = Boletin.objects.select_related(
                "estudiante__id_persona",
                "periodo_academico"
            ).get(id_boletin=id_boletin)
        except Boletin.DoesNotExist:
            return HttpResponse(
                b"Boletin no encontrado",
                status=status.HTTP_404_NOT_FOUND
            )

        estudiante = Estudiante.objects.get(id_persona=id_persona)

        persona = estudiante.get_id_persona()

        def nombre_completo_persona(persona_obj):
            if not persona_obj:
                return ""
            parts = [
                persona_obj.get_primer_nombre() or "",
                persona_obj.get_segundo_nombre() or "",
                persona_obj.get_primer_apellido() or "",
                persona_obj.get_segundo_apellido() or "",
            ]
            return " ".join([p for p in parts if p]).strip()

        nombre_estudiante = nombre_completo_persona(persona)

        acudiente_obj = estudiante.get_acudiente()
        nombre_acudiente = ""

        if acudiente_obj:
            try:
                persona_acu = acudiente_obj.get_persona()
            except Exception:
                persona_acu = getattr(acudiente_obj, "id_persona", None)

            nombre_acudiente = nombre_completo_persona(persona_acu) if persona_acu else ""

        nombre_grupo = boletin.get_nombre_grupo() or ""
        profesor_director = boletin.get_profesor_director() or ""
        anio = getattr(boletin.get_periodo_academico(), "anio", "")

        # Evaluaciones
        evals = Evaluacion.objects.select_related(
            "logro__categoria_logros"
        ).filter(
            boletin=boletin
        ).order_by(
            "logro__categoria_logros__id_categoria_logros",
            "logro__id_logro"
        )

        categorias = defaultdict(list)
        for e in evals:
            cat = e.get_logro().get_categoria_logros()
            cat_name = cat.get_nombre_categoria() if cat else "Sin categoría"
            categorias[cat_name].append({
                "concepto": e.get_logro().get_concepto_logro(),
                "descripcion": e.get_logro().get_descripcion_logro(),
                "c1": e.get_evaluacion_corte1(),
                "c2": e.get_evaluacion_corte2(),
                "c3": e.get_evaluacion_corte3(),
            })

        # PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )

        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]
        style_h1 = ParagraphStyle("h1", parent=styles["Heading1"], alignment=1, spaceAfter=6)
        style_bold = ParagraphStyle("bold", parent=style_normal, fontName="Helvetica-Bold")
        style_small = ParagraphStyle("small", parent=style_normal, fontSize=9)

        story = []

        story.append(Paragraph("Instituto Primera Infancia", style_h1))
        story.append(Spacer(1, 6))

        s1 = Table([
            [
                Paragraph("<b>Estudiante:</b> " + (nombre_estudiante or " — "),
                          style_normal),
                Paragraph("<b>Acudiente:</b> " + (nombre_acudiente or " — "),
                          style_normal)
            ]
        ], colWidths=[100 * mm, 70 * mm])

        s1.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(s1)
        story.append(Spacer(1, 8))

        s2 = Table([
            [
                Paragraph("<b>Grupo:</b> " + (nombre_grupo or " — "), style_normal),
                Paragraph("<b>Profesor:</b> " + (profesor_director or " — "), style_normal),
                Paragraph("<b>Periodo (Año):</b> " + str(anio or " — "), style_normal)
            ]
        ], colWidths=[65 * mm, 65 * mm, 40 * mm])

        s2.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(s2)
        story.append(Spacer(1, 10))

        for cat_name, items in categorias.items():
            story.append(Paragraph(f"<b>{cat_name}</b>", style_bold))
            story.append(Spacer(1, 6))

            data = [["Logro", "Corte 1", "Corte 2", "Corte 3"]]

            for it in items:
                data.append([
                    Paragraph(it["concepto"] or "", style_small),
                    it["c1"] or "",
                    it["c2"] or "",
                    it["c3"] or "",
                ])

            t = Table(data, colWidths=[90 * mm, 25 * mm, 25 * mm, 25 * mm], repeatRows=1)

            t.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))

            story.append(KeepTogether(t))
            story.append(Spacer(1, 10))

        if not categorias:
            story.append(Paragraph("No hay evaluaciones registradas para este boletín.", style_normal))

        doc.build(story)

        pdf = buffer.getvalue()
        buffer.close()

        filename = f"boletin_{boletin.get_id_boletin()}.pdf"

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response
