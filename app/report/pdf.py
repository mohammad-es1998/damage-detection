from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(car, image_path, pdf_path):
    c = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Car details table
    car_data = [
        ['Plate', car.plate],
        ['Model', car.model],
        ['Color', car.color],
        ['VIN', car.vin],
        ['Brand', car.brand]
    ]

    car_table = Table(car_data, colWidths=[1.5 * inch, 3 * inch])
    car_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(car_table)

    # Space between tables
    elements.append(Spacer(1, 0.5 * inch))

    # Image
    elements.append(Image(image_path, 3 * inch, 3 * inch))

    # Space between image and damages table
    elements.append(Spacer(1, 0.5 * inch))

    # Damages table
    damage_data = [['Part', 'Damage Type']]
    for damage in car.damages:
        damage_data.append([damage.part, damage.damage_type])

    damage_table = Table(damage_data, colWidths=[2.5 * inch, 2.5 * inch])
    damage_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(damage_table)

    # Build the PDF
    c.build(elements)
