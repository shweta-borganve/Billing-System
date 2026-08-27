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

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    )
    assert cursor.fetchone() is not None

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bills'")
    assert cursor.fetchone() is not None

    conn.close()


def test_get_all_bills_empty(temp_db):
    """Test fetching bills when the table is empty."""
    bills = get_all_bills()
    assert bills == []


def test_get_all_bills_with_data(temp_db):
    """Test fetching bills with valid JSON items data."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 150.0, json.dumps([{"item": "Pen", "qty": 2}])),
    )
    conn.commit()
    conn.close()

    bills = get_all_bills()
    assert len(bills) == 1
    assert bills[0]["total_amount"] == 150.0
    assert bills[0]["items"] == [{"item": "Pen", "qty": 2}]


def test_update_product_quantity(temp_db):
    """Test reducing product quantity after a sale."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Notebook', 25.0, 100)"
    )
    conn.commit()
    conn.close()

    update_product_quantity(1, 10)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM products WHERE id = 1")
    row = cursor.fetchone()
    conn.close()

    assert row[0] == 90


def test_initialize_database_exception(monkeypatch):
    """Test exception handling during database initialization."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection failed")):
        initialize_database()


def test_get_all_bills_exception():
    """Test exception handling when fetching bills fails to trigger lines 34-35."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Fetch failed")):
        bills = get_all_bills()
        assert bills == []


def test_update_product_quantity_exception(temp_db):
    """Test exception handling when updating product quantity fails."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Update failed")):
        update_product_quantity(1, 5)
