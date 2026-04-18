from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generar_pdf(ip, riesgos, recomendaciones):

    ruta = "app/static/reportes/reporte.pdf"

    doc = SimpleDocTemplate(
        ruta,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    estilos = getSampleStyleSheet()
    elementos = []

    # ===============================
    # PORTADA
    # ===============================
    elementos.append(
        Paragraph(
            "<font size=24><b>SecureScan</b></font>",
            estilos["Title"]
        )
    )

    elementos.append(Spacer(1, 15))

    elementos.append(
        Paragraph(
            "<font size=16 color='gray'>Reporte Ejecutivo de Ciberseguridad</font>",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 30))

    elementos.append(
        Paragraph(
            f"<b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Objetivo Analizado:</b> {ip}",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 30))

    # ===============================
    # RESUMEN
    # ===============================
    elementos.append(
        Paragraph(
            "<font size=16><b>Resumen Ejecutivo</b></font>",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "Se ejecutó un análisis automatizado de seguridad para identificar "
            "riesgos operativos y técnicos asociados al objetivo evaluado.",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 25))

    # ===============================
    # TABLA RIESGOS
    # ===============================
    elementos.append(
        Paragraph(
            "<font size=16><b>Riesgos Detectados</b></font>",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    data = [["#", "Descripción"]]

    for i, r in enumerate(riesgos, start=1):
        data.append([str(i), r])

    tabla = Table(data, colWidths=[40, 470])

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elementos.append(tabla)

    elementos.append(Spacer(1, 25))

    # ===============================
    # RECOMENDACIONES
    # ===============================
    elementos.append(
        Paragraph(
            "<font size=16><b>Recomendaciones Estratégicas</b></font>",
            estilos["Heading2"]
        )
    )

    elementos.append(Spacer(1, 10))

    for rec in recomendaciones:
        elementos.append(
            Paragraph(f"• {rec}", estilos["Normal"])
        )

    elementos.append(Spacer(1, 30))

    # ===============================
    # FOOTER
    # ===============================
    elementos.append(
        Paragraph(
            "<font size=10 color='gray'>Documento generado automáticamente por SecureScan</font>",
            estilos["Normal"]
        )
    )

    doc.build(elementos)

    return ruta