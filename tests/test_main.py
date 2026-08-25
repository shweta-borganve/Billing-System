import runpy
import sqlite3
from unittest.mock import patch

import pytest

from src.services.main import check_and_display_low_stock, main


@pytest.fixture
def mock_main_dependencies(monkeypatch):
    """Fixture to mock out external dependencies for main execution tests."""
    monkeypatch.setattr("src.services.main.login", lambda: True)
    monkeypatch.setattr("src.database.db_operations.initialize_database", lambda: None)
    monkeypatch.setattr("src.services.main.check_and_display_low_stock", lambda: None)


def test_check_and_display_low_stock_with_items(monkeypatch):
    """Test low stock display logic when low stock items are present."""
    mock_cursor = patch("sqlite3.Cursor").start()
    mock_cursor.fetchall.return_value = [("Pen", 2), ("Notebook", 1)]

    mock_conn = patch("sqlite3.connect").start()
    mock_conn.return_value.cursor.return_value = mock_cursor

    check_and_display_low_stock()
    patch.stopall()


def test_check_and_display_low_stock_sqlite_error(monkeypatch):
    """Test database error handling inside low stock check."""
    with patch("sqlite3.connect", side_effect=sqlite3.Error("DB error")):
        check_and_display_low_stock()


def test_main_login_failure(monkeypatch):
    """Test main function when login returns False."""
    monkeypatch.setattr("src.services.main.login", lambda: False)
    main()


def test_main_menu_all_options(mock_main_dependencies, monkeypatch):
    """Test every menu option choice, invalid options, and errors."""
    monkeypatch.setattr("src.services.main.add_product", lambda: None)
    monkeypatch.setattr("src.services.main.view_products", lambda: None)
    monkeypatch.setattr("src.services.main.search_product", lambda: None)
    monkeypatch.setattr("src.services.main.update_product", lambda: None)
    monkeypatch.setattr("src.services.main.delete_product", lambda: None)
    monkeypatch.setattr("src.services.main.generate_bill", lambda: None)
    monkeypatch.setattr("src.services.main.view_bill_history", lambda: None)
    monkeypatch.setattr("src.services.main.check_and_display_low_stock", lambda: None)
    monkeypatch.setattr("src.services.main.generate_sales_report", lambda: None)

    inputs = iter(["99", "abc"] + [str(i) for i in range(1, 11)])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()


def test_main_script_execution(monkeypatch):
    """Test running main.py as a script block (__main__)."""
    monkeypatch.setattr("src.auth.auth.login", lambda: False)
    monkeypatch.setattr("sys.argv", ["main.py"])
    try:
        runpy.run_module("src.services.main", run_name="__main__")
    except SystemExit:
        pass
