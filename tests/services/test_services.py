import json
import sqlite3
from unittest.mock import patch

import pytest

from src.services import config, file_handler, history, logger_config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Fixture to use a temporary database for file handler and history testing."""
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
    conn.commit()
    conn.close()
    return db_file


def test_logger_setup():
    """Test that the logger module returns a valid logger instance."""
    logger = logger_config.logger
    assert logger is not None


# --- HISTORY TESTS ---
def test_view_bill_history_empty(temp_db):
    history.view_bill_history()


def test_view_bill_history_with_data(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    valid_items = json.dumps([{"name": "Notebook", "quantity": 3, "amount": 150.0}])
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 150.0, valid_items),
    )
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-02", 20.0, "not-a-json"),
    )
    conn.commit()
    conn.close()
    history.view_bill_history()


def test_view_bill_history_sqlite_error():
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection error")):
        history.view_bill_history()


# --- FILE HANDLER TESTS ---
def test_load_data_bills(temp_db):
    """Test loading bills via file_handler."""
    # Test with string 'bills' or constant
    res = file_handler.load_data("bills.json")
    assert isinstance(res, list)


def test_load_data_products(temp_db):
    """Test loading products via file_handler."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Pen', 10.0, 50)"
    )
    conn.commit()
    conn.close()

    res = file_handler.load_data("products.json")
    assert len(res) == 1
    assert res[0]["name"] == "Pen"


def test_load_data_fallback(temp_db):
    """Test loading unknown file type returns empty list."""
    res = file_handler.load_data("unknown_file.json")
    assert res == []


def test_load_data_error(temp_db):
    """Test exception handling during load_data."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("DB Load Error")):
        res = file_handler.load_data("products.json")
        assert res == []


def test_save_data_products(temp_db):
    """Test saving products via file_handler."""
    products_data = [{"product_id": 1, "name": "Book", "price": 100.0, "quantity": 10}]
    file_handler.save_data("products.json", products_data)

    loaded = file_handler.load_data("products.json")
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Book"


def test_save_data_fallback(temp_db):
    """Test saving non-product file skips execution safely."""
    file_handler.save_data("unknown.json", [])


def test_save_data_error(temp_db):
    """Test exception handling during save_data."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("DB Save Error")):
        file_handler.save_data("products.json", [])


def test_save_bill_record_list_items(temp_db):
    """Test saving bill with a list of items."""
    items = [{"name": "Eraser", "quantity": 5, "amount": 25.0}]
    file_handler.save_bill_record("bills.json", items, 25.0, "2026-06-01")


def test_save_bill_record_string_items(temp_db):
    """Test saving bill with valid JSON string items."""
    items_str = json.dumps([{"name": "Ruler", "quantity": 1, "amount": 15.0}])
    file_handler.save_bill_record("bills.json", items_str, 15.0, "2026-06-01")


def test_save_bill_record_malformed_string_items(temp_db):
    """Test saving bill with malformed string items triggering JSONDecodeError pass."""
    file_handler.save_bill_record(
        "bills.json", "invalid-json-string", 0.0, "2026-06-01"
    )


def test_save_bill_record_error(temp_db):
    """Test exception handling during save_bill_record."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("DB Bill Error")):
        file_handler.save_bill_record("bills.json", [], 0.0, "2026-06-01")
