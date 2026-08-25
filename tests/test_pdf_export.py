import os
from src.billing.pdf_export import generate_pdf_receipt


def test_generate_pdf_receipt(tmp_path):
    """Test generating a PDF receipt successfully."""
    pdf_file = tmp_path / "test_receipt.pdf"
    
    bill_id = 101
    date_str = "2026-03-31 12:00:00"
    items = [
        {"name": "Notebook", "price": 50.00, "quantity": 2, "amount": 100.00},
        {"name": "Pen", "price": 10.50, "quantity": 4, "amount": 42.00},
    ]
    total = 142.00

    # Execute PDF generation
    generate_pdf_receipt(str(pdf_file), bill_id, date_str, items, total)

    # Assertions
    assert os.path.exists(pdf_file)
    assert os.path.getsize(pdf_file) > 0 