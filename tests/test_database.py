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
    ):
        try:
            database.initialize_database()
        except sqlite3.Error:
            pass


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
