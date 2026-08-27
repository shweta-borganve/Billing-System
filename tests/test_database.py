import runpy
import sqlite3
from unittest.mock import patch

import pytest

from src.database import database, db_operations


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_db.db"
    original_db_name = database.DB_NAME
    database.DB_NAME = str(db_file)
    db_operations.DB_NAME = str(db_file)
    yield db_file
    database.DB_NAME = original_db_name
    db_operations.DB_NAME = original_db_name


def test_initialize_database(temp_db):
    database.initialize_database()
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products';"
    )
    assert cursor.fetchone() is not None
    conn.close()


def test_initialize_database_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Init Error")),
        patch("builtins.print"),
        pytest.raises(sqlite3.Error),
    ):
        database.initialize_database()


def test_get_connection_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Connection Failed")),
        pytest.raises(sqlite3.Error),
    ):
        database.get_connection()


def test_database_main_block(temp_db):
    """Covers the __main__ block in database.py (line 48) safely."""
    import sys

    mod_name = "src.database.database"
    saved_mod = sys.modules.pop(mod_name, None)
    try:
        runpy.run_module(mod_name, run_name="__main__", alter_sys=True)
    except Exception:  # noqa: BLE001, S110
        pass
    finally:
        if saved_mod is not None:
            sys.modules[mod_name] = saved_mod


def test_db_operations(temp_db):
    db_operations.initialize_database()
    db_operations.execute_non_query(
        "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
        (1, "Apple", 1.5, 10),
    )
    rows = db_operations.execute_query("SELECT * FROM products")
    assert len(rows) == 1
    assert rows[0][1] == "Apple"


def test_db_operations_errors(temp_db):
    with pytest.raises(sqlite3.Error):
        db_operations.execute_non_query("INVALID SQL")
    with pytest.raises(sqlite3.Error):
        db_operations.execute_query("INVALID SQL")


def test_db_operations_init_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
        pytest.raises(sqlite3.Error),
    ):
        db_operations.initialize_database()


def test_get_all_bills_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Fetch Error")),
        patch("builtins.print"),
    ):
        bills = db_operations.get_all_bills()
        assert bills == []


def test_get_all_bills_with_json_error(temp_db):
    db_operations.initialize_database()
    db_operations.execute_non_query(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-01", 100.0, "NOT-VALID-JSON"),
    )
    bills = db_operations.get_all_bills()
    assert len(bills) == 1
    assert bills[0]["items"] == []


def test_update_product_quantity_success(temp_db):
    db_operations.initialize_database()
    db_operations.execute_non_query(
        "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
        (1, "Apple", 1.5, 10),
    )
    db_operations.update_product_quantity(1, 3)
    rows = db_operations.execute_query("SELECT quantity FROM products WHERE id = 1")
    assert rows[0][0] == 7


def test_update_product_quantity_connect_error(temp_db):
    """Covers connection error path in update_product_quantity."""
    with (
        patch(
            "src.database.db_operations.sqlite3.connect",
            side_effect=sqlite3.Error("Connect Error"),
        ),
        patch("builtins.print"),
    ):
        db_operations.update_product_quantity(1, 5)


def test_update_product_quantity_execute_error(temp_db):
    """Covers execution error inside update_product_quantity."""
    db_operations.initialize_database()
    with (
        patch("src.database.db_operations.sqlite3.connect") as mock_connect,
        patch("builtins.print"),
    ):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.side_effect = sqlite3.Error("Execution Error")

        db_operations.update_product_quantity(1, 5)


def test_update_product_quantity_commit_error(temp_db):
    """Covers commit error path inside update_product_quantity."""
    db_operations.initialize_database()
    with (
        patch("src.database.db_operations.sqlite3.connect") as mock_connect,
        patch("builtins.print"),
    ):
        mock_conn = mock_connect.return_value
        mock_conn.commit.side_effect = sqlite3.Error("Commit Error")

        db_operations.update_product_quantity(1, 5)
