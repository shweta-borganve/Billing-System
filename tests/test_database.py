import sqlite3
from unittest.mock import patch

import pytest

from src.database import database, db_operations
from src.services import config


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_db.db"
    original_db_name = config.DB_NAME
    config.DB_NAME = str(db_file)
    database.initialize_database()
    yield str(db_file)
    config.DB_NAME = original_db_name


def test_database_connection_errors():
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Connection failed")),
        pytest.raises(sqlite3.Error),
    ):
        database.get_connection()


def test_initialize_database_error():
    with (
feature/bandit-security-scanning
        patch("sqlite3.connect", side_effect=sqlite3.Error("Init Error")),
        pytest.raises(sqlite3.Error, match="Init Error"),

        patch(
            "src.database.database.get_connection",
            side_effect=sqlite3.Error("Init failed"),
        ),
        pytest.raises(sqlite3.Error),
main
    ):
        database.initialize_database()


def test_db_operations_full_coverage(temp_db):
    db_operations.execute_non_query(
        "CREATE TABLE IF NOT EXISTS test_tbl (id INTEGER PRIMARY KEY, val TEXT)"
    )
    db_operations.execute_non_query("INSERT INTO test_tbl (val) VALUES (?)", ("hello",))

    rows = db_operations.execute_query("SELECT * FROM test_tbl")
    assert len(rows) == 1

    db_operations.update_product_quantity(1, 1)

    bills = db_operations.get_all_bills()
    assert isinstance(bills, list)

    with patch("sqlite3.connect", side_effect=sqlite3.Error("Operation failed")):
        assert db_operations.execute_non_query("SELECT 1") is None
        assert db_operations.execute_query("SELECT 1") == []
        assert db_operations.update_product_quantity(1, 5) is None

    with patch("sqlite3.connect", side_effect=sqlite3.Error("Fetch bills error")):
        assert db_operations.get_all_bills() == []

    with patch("sqlite3.connect", side_effect=sqlite3.Error("Connection error")):
        assert database.get_all_bills() == []


def test_db_operations_invalid_json(temp_db):
    db_operations.execute_non_query(
        "INSERT INTO bills (bill_details, total_amount, timestamp) VALUES (?, ?, ?)",
        ("invalid_json_string", 50.0, "2026-03-30 10:00:00"),
    )
    bills = db_operations.get_all_bills()
    assert isinstance(bills, list)
    assert len(bills) == 1
    assert bills[0]["items"] == []


def test_database_get_all_bills_and_operations(temp_db):
    database.initialize_database()
    bills = database.get_all_bills()
    assert isinstance(bills, list)


def test_database_get_all_bills_exception_handling():
    with patch("src.database.database.sqlite3.connect") as mock_connect:
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.side_effect = sqlite3.Error("Execution error")
        assert database.get_all_bills() == []
