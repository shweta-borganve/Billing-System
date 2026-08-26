import json
import sqlite3
from unittest.mock import patch

import pytest

from src.billing import analytics
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Fixture to use a temporary database for analytics testing."""
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
    conn.commit()
    conn.close()
    return db_file


def test_generate_sales_report_empty(temp_db):
    """Test sales report when no bills exist."""
    analytics.generate_sales_report()


def test_generate_sales_report_with_data(temp_db):
    """Test sales report with valid bill data and items."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    valid_items = json.dumps([{"name": "Pen", "quantity": 2, "amount": 20.0}])
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 20.0, valid_items),
    )
    conn.commit()
    conn.close()

    analytics.generate_sales_report()


def test_generate_sales_report_malformed_and_empty_items(temp_db):
    """Test sales report with malformed JSON and empty item lists."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Malformed JSON to trigger JSONDecodeError exception and continue
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-02", 10.0, "bad-json"),
    )

    # Valid row but empty items array to test the 'No item data recorded' branch
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-03", 15.0, json.dumps([])),
    )

    conn.commit()
    conn.close()

    analytics.generate_sales_report()


def test_generate_sales_report_sqlite_error(temp_db):
    """Test database error handling during sales report generation."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Analytics DB Error")):
        analytics.generate_sales_report()
