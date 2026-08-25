import json
import sqlite3
from unittest.mock import patch

import pytest

from src.database.database import initialize_database
from src.database.db_operations import (
    get_all_bills,
    update_product_quantity,
)
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Fixture to use a temporary database for testing."""
    db_file = tmp_path / "test_billing.db"
    monkeypatch.setattr(config, "DB_NAME", str(db_file))
    initialize_database()
    return db_file


def test_initialize_database(temp_db):
    """Test that database tables are successfully created."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Check products table
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    )
    assert cursor.fetchone() is not None

    # Check bills table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bills'")
    assert cursor.fetchone() is not None

    conn.close()


def test_get_all_bills_empty(temp_db):
    """Test fetching bills when the table is empty."""
    bills = get_all_bills()
    assert bills == []


def test_get_all_bills_with_data(temp_db):
    """Test fetching bills with valid and invalid JSON items data."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    # Insert a bill with valid JSON items
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 150.0, json.dumps([{"item": "Pen", "qty": 2}])),
    )

    # Insert a bill with invalid JSON string to trigger JSONDecodeError branch
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-02", 50.0, "not-a-json-string"),
    )

    conn.commit()
    conn.close()

    bills = get_all_bills()
    assert len(bills) == 2
    assert bills[0]["total_amount"] == 150.0
    assert bills[0]["items"] == [{"item": "Pen", "qty": 2}]
    # Invalid JSON should fall back to an empty list
    assert bills[1]["items"] == []


def test_update_product_quantity(temp_db):
    """Test reducing product quantity after a sale."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Notebook', 25.0, 100)"
    )
    conn.commit()
    conn.close()

    # Update quantity (sell 10)
    update_product_quantity(1, 10)

    # Verify new quantity
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM products WHERE id = 1")
    row = cursor.fetchone()
    conn.close()

    assert row[0] == 90


def test_initialize_database_exception(monkeypatch):
    """Test exception handling during database initialization."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection failed")):
        # Should catch the exception gracefully and complete without failing
        initialize_database()


def test_get_all_bills_exception(temp_db):
    """Test exception handling when fetching bills fails."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Fetch failed")):
        bills = get_all_bills()
        assert bills == []


def test_update_product_quantity_exception(temp_db):
    """Test exception handling when updating product quantity fails."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Update failed")):
        # Should catch the exception gracefully
        update_product_quantity(1, 5)
