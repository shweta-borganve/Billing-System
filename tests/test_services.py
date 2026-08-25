import json
import sqlite3
from unittest.mock import patch

import pytest

from src.services import config, history, logger_config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Fixture to use a temporary database for history testing."""
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


def test_logger_setup():
    """Test that the logger module returns a valid logger instance."""
    logger = logger_config.logger
    assert logger is not None


def test_view_bill_history_empty(temp_db):
    """Test viewing bill history when no bills exist."""
    history.view_bill_history()


def test_view_bill_history_with_data(temp_db):
    """Test viewing bill history with valid JSON and malformed JSON rows."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Valid JSON string items with proper keys to trigger the inner loop
    valid_items = json.dumps([{"name": "Notebook", "quantity": 3, "amount": 150.0}])
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 150.0, valid_items),
    )

    # Malformed JSON string to test JSONDecodeError exception fallback
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-02", 20.0, "not-a-json"),
    )

    conn.commit()
    conn.close()

    history.view_bill_history()


def test_view_bill_history_sqlite_error():
    """Test handling of database errors when viewing history."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection error")):
        history.view_bill_history()
