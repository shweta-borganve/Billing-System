from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_receipt(filename, bill_id, date_str, items, total):
    """Generates a professional PDF receipt using ReportLab."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=20,
        spaceAfter=6,
        alignment=1,  # Centered
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=15,
        alignment=1,
    )

    # Header Info
    story.append(Paragraph("<b>STORE INVOICE / RECEIPT</b>", title_style))
    story.append(Paragraph(f"Bill ID: {bill_id} | Date: {date_str}", subtitle_style))
    story.append(Spacer(1, 10))

    # Table Data Construction
    table_data = [["Item Name", "Price", "Qty", "Amount"]]
    for item in items:
        table_data.append(
            [
                item["name"],
                f"₹{item['price']:.2f}",
                str(item["quantity"]),
                f"₹{item['amount']:.2f}",
            ]
        )

    # Add Total row
    table_data.append(["", "", "Total:", f"₹{total:.2f}"])

    # Table Styling
    t = Table(table_data, colWidths=[250, 90, 60, 100])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
                ("LINEABOVE", (2, -1), (-1, -1), 1, colors.black),
                ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
            ]
        )
    )

    story.append(t)
    doc.build(story)
