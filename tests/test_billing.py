import json
import sqlite3
from unittest.mock import patch

import pytest

from src.billing import billing
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Fixture to use a temporary database for billing testing."""
    db_file = tmp_path / "test_billing.db"
    monkeypatch.setattr(config, "DB_NAME", str(db_file))
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Pen', 10.0, 10)"
    )
    conn.commit()
    conn.close()
    return db_file


def test_check_low_stock_in_list():
    """Test low stock checker helper function."""
    products = [
        {"name": "Pen", "quantity": 2},
        {"name": "Book", "quantity": 10},
    ]
    low_items = billing.check_low_stock_in_list(products, threshold=5)
    assert len(low_items) == 1
    assert low_items[0] == ("Pen", 2)


def test_generate_bill_no_products(temp_db, monkeypatch):
    """Test generating bill when no products exist."""
    monkeypatch.setattr("src.billing.billing.load_data", lambda f: [])
    billing.generate_bill()


def test_generate_bill_no_items_added(temp_db):
    """Test generating bill when user immediately finishes without adding items."""
    inputs = iter(["0"])
    with patch("builtins.input", lambda _: next(inputs)):
        billing.generate_bill()


def test_generate_bill_success_with_low_stock_alert(temp_db):
    """Successful bill generation flow that triggers the low stock alert (remaining <= 5)."""
    inputs = iter(["1", "6", "0"])
    with patch("builtins.input", lambda _: next(inputs)):
        billing.generate_bill()


def test_generate_bill_invalid_inputs_and_errors(temp_db):
    """Test handling of invalid quantity, insufficient stock, invalid product ID, and ValueError."""
    inputs = iter(["999", "abc", "1", "-1", "1", "15", "1", "1", "0"])
    with patch("builtins.input", lambda _: next(inputs)):
        billing.generate_bill()


def test_generate_bill_sqlite_error_exact(temp_db):
    """Explicitly test sqlite3.Error block when saving a bill (lines 86-87)."""
    inputs = iter(["1", "1", "0"])
    with (
        patch("builtins.input", lambda _: next(inputs)),
        patch(
            "src.billing.billing.sqlite3.connect",
            side_effect=sqlite3.Error("Intentional DB Save Error"),
        ),
    ):
        billing.generate_bill()


def test_generate_bill_pdf_exception_exact(temp_db):
    """Test handling of exception during PDF generation (lines 111-114)."""
    inputs = iter(["1", "1", "0"])
    with (
        patch("builtins.input", lambda _: next(inputs)),
        patch(
            "src.billing.billing.generate_pdf_receipt",
            side_effect=Exception("Intentional PDF Exception"),
        ),
    ):
        billing.generate_bill()


def test_view_bill_history_empty(temp_db):
    """Test viewing empty bill history."""
    billing.view_bill_history()


def test_view_bill_history_with_data(temp_db):
    """Test viewing bill history with valid and malformed item records."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    valid_items = json.dumps([{"name": "Pen", "quantity": 1, "amount": 10.0}])
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01 10:00:00", 10.0, valid_items),
    )
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01 11:00:00", 5.0, "bad-json"),
    )
    conn.commit()
    conn.close()

    billing.view_bill_history()


def test_view_bill_history_sqlite_error_exact(temp_db):
    """Explicitly test sqlite3.Error block when viewing bill history."""
    with patch(
        "src.billing.billing.sqlite3.connect",
        side_effect=sqlite3.Error("Intentional History DB Error"),
    ):
        billing.view_bill_history()
