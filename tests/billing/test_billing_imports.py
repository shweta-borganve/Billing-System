def test_application_billing_imports():
    from src.billing.analytics import generate_sales_report
    from src.billing.pdf_export import generate_pdf_receipt

    assert generate_sales_report is not None
    assert generate_pdf_receipt is not None
