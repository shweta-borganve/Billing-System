import sqlite3
from unittest.mock import patch

import pytest

from src.database import database, db_operations
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_db.db"
    monkeypatch.setattr(config, "DB_NAME", str(db_file))
    return db_file


def test_get_connection(temp_db):
    conn = database.get_connection()
    assert conn is not None
    conn.close()


def test_initialize_database(temp_db):
    database.initialize_database()


def test_initialize_database_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Init Error")),
        patch("builtins.print"),
    ):
        database.initialize_database()


def test_db_operations(temp_db):
    db_operations.execute_non_query("CREATE TABLE test (id INT)")
    res = db_operations.execute_query("SELECT * FROM test")
    assert res == []


def test_db_operations_errors(temp_db):
    with pytest.raises(sqlite3.Error):
        db_operations.execute_non_query("INVALID SQL")
    with pytest.raises(sqlite3.Error):
        db_operations.execute_query("INVALID SQL")


def test_get_all_bills_error(temp_db):
    with patch("sqlite3.connect", side_effect=sqlite3.Error("Bills Error")):
        res = db_operations.get_all_bills()
        assert res == []
