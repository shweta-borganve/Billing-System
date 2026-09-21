import sqlite3
import pytest
from src.database.database import DB_NAME, get_connection, initialize_database


def test_get_connection(monkeypatch, tmp_path):
    # Redirect DB_NAME to a temporary file path
    temp_db = tmp_path / "test_billing.db"
    monkeypatch.setattr("src.database.database.DB_NAME", str(temp_db))

    conn = get_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_initialize_database(monkeypatch, tmp_path):
    # Redirect DB_NAME to a temporary file path
    temp_db = tmp_path / "test_billing.db"
    monkeypatch.setattr("src.database.database.DB_NAME", str(temp_db))

    # Run initialization
    initialize_database()

    # Verify tables were created successfully
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()

    # Check products table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products';"
    )
    assert cursor.fetchone() is not None

    # Check bills table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bills';"
    )
    assert cursor.fetchone() is not None

    conn.close() 