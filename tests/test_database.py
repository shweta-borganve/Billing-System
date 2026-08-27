import json
import sqlite3
from unittest.mock import patch

import pytest

from src.database import database, db_operations


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_db.db"
    with patch("src.services.config.DB_NAME", str(db_file)):
        yield db_file


def test_initialize_database_success(temp_db):
    """Test successful database initialization."""
    database.initialize_database()


def test_initialize_database_error(temp_db):
    """Test database initialization error handling."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Init Error")):
        database.initialize_database()


def test_db_operations_initialize_database_stub():
    """Test db_operations stub initialize function."""
    db_operations.initialize_database()


def test_execute_non_query_success(temp_db):
    """Test successful execution of non-query operations."""
    db_operations.execute_non_query(
        "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
        (1, "Apple", 10.0, 50),
    )
    result = db_operations.execute_query("SELECT * FROM products WHERE id = ?", (1,))
    assert len(result) == 1
    assert result[0][1] == "Apple"


def test_execute_non_query_error(temp_db):
    """Test execute_non_query handles sqlite3.Error."""
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Non-query Error")),
        pytest.raises(sqlite3.Error),
    ):
        db_operations.execute_non_query("SELECT 1")


def test_execute_query_error(temp_db):
    """Test execute_query handles sqlite3.Error."""
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Query Error")),
        pytest.raises(sqlite3.Error),
    ):
        db_operations.execute_query("SELECT 1")


def test_get_all_bills_success(temp_db):
    """Test fetching all bills successfully."""
    db_operations.execute_non_query(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-06", 150.0, json.dumps([{"item": "apple", "qty": 2}])),
    )
    bills = db_operations.get_all_bills()
    assert len(bills) == 1
    assert bills[0]["total_amount"] == 150.0
    assert len(bills[0]["items"]) == 1


def test_get_all_bills_db_error(temp_db):
    """Test get_all_bills handles sqlite3.Error and returns empty list."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Fetch Bills Error")):
        bills = db_operations.get_all_bills()
        assert bills == []


def test_get_all_bills_json_decode_error(temp_db):
    """Test get_all_bills handles invalid JSON gracefully."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-06", 100.0, "CORRUPTED_JSON"),
    )
    conn.commit()
    conn.close()

    with patch("src.services.config.DB_NAME", str(temp_db)):
        bills = db_operations.get_all_bills()
        assert len(bills) == 1
        assert bills[0]["items"] == []


def test_update_product_quantity_success(temp_db):
    """Test successful product quantity update."""
    db_operations.execute_non_query(
        "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
        (2, "Banana", 5.0, 20),
    )
    db_operations.update_product_quantity(2, 5)
    result = db_operations.execute_query(
        "SELECT quantity FROM products WHERE id = ?", (2,)
    )
    assert result[0][0] == 15


def test_update_product_quantity_error(temp_db):
    """Test update_product_quantity handles sqlite3.Error."""
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Update Error")),
        patch("builtins.print") as mock_print,
    ):
        db_operations.update_product_quantity(1, 5)
        mock_print.assert_called()
