import sqlite3

import pytest

from src.services.main import check_and_display_low_stock, main


@pytest.fixture
def mock_main_dependencies(monkeypatch):
    monkeypatch.setattr("src.services.main.login", lambda: True)
    monkeypatch.setattr("src.services.main.initialize_database", lambda: None)


def test_main_success_flow(mock_main_dependencies, monkeypatch, capsys):
    """Test successful login and immediate exit."""
    inputs = iter(["0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()
    captured = capsys.readouterr()
    assert "Billing System Menu" in captured.out


def test_main_login_failure(monkeypatch, capsys):
    """Test handling of failed login."""
    monkeypatch.setattr("src.services.main.login", lambda: False)

    main()
    captured = capsys.readouterr()
    assert "Authentication failed" in captured.out


def test_main_menu_all_options(mock_main_dependencies, monkeypatch, capsys):
    """Test every menu option choice, invalid options, and errors."""
    monkeypatch.setattr("src.services.main.add_product", lambda: None)
    monkeypatch.setattr("src.services.main.view_products", lambda: None)
    monkeypatch.setattr("src.services.main.search_product", lambda: None)
    monkeypatch.setattr("src.services.main.update_product", lambda: None)
    monkeypatch.setattr("src.services.main.delete_product", lambda: None)
    monkeypatch.setattr("src.services.main.generate_bill", lambda: None)
    monkeypatch.setattr("src.services.main.view_bill_history", lambda: None)
    monkeypatch.setattr("src.services.main.generate_sales_report", lambda: None)
    monkeypatch.setattr("src.services.main.check_and_display_low_stock", lambda: None)

    inputs = iter(["1", "2", "3", "4", "5", "6", "7", "8", "9", "invalid", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main()
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out
    assert "Exiting application" in captured.out


def test_check_and_display_low_stock(monkeypatch, capsys):
    """Test low stock warning display function."""

    class MockCursor:
        def execute(self, query):
            pass

        def fetchall(self):
            return [("Item A", 2), ("Item B", 1)]

    class MockConn:
        def cursor(self):
            return MockCursor()

        def close(self):
            pass

    monkeypatch.setattr("sqlite3.connect", lambda _: MockConn())

    check_and_display_low_stock()
    captured = capsys.readouterr()
    assert "Low Stock Warnings" in captured.out
    assert "Item A" in captured.out


def test_check_and_display_low_stock_exception(monkeypatch):
    """Test low stock exception handling."""

    def mock_connect(*args, **kwargs):
        raise sqlite3.Error("DB error")

    monkeypatch.setattr("sqlite3.connect", mock_connect)
    # Should safely log and catch the exception without crashing
    check_and_display_low_stock()
