import sqlite3

import pytest

from src.services.main import check_and_display_low_stock, main


@pytest.fixture
def mock_main_dependencies(monkeypatch):
    monkeypatch.setattr("src.services.main.login", lambda: True)
    monkeypatch.setattr("src.services.main.initialize_database", lambda: None)


def test_main_success_flow(mock_main_dependencies, monkeypatch, capsys):
    """Test successful login and immediate exit."""
    inputs = iter(["10"])
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
    monkeypatch.setattr("src.services.main.create_bill", lambda: None)

    inputs = iter(["1", "2", "3", "4", "5", "6", "7", "8", "9", "invalid", "10"])
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


def test_create_bill_success(monkeypatch, capsys):
    """Test successful bill creation."""
    products = [
        (1, "Pen", 100.0, 10),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    added_items = []

    def mock_add_item(cart, product_data, quantity):
        cart.append(product_data)
        added_items.append((product_data, quantity))

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        mock_add_item,
    )

    generated_bills = []
    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: generated_bills.append(cart),
    )

    inputs = iter(["1", "2", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Added 2 x Pen to cart." in captured.out
    assert added_items[0][1] == 2
    assert generated_bills[0][0]["name"] == "Pen"


def test_create_bill_no_products(monkeypatch):
    """Test bill creation when no products are available."""
    monkeypatch.setattr("src.services.main.view_products", lambda: [])

    from src.services.main import create_bill

    create_bill()


def test_create_bill_invalid_quantity(monkeypatch, capsys):
    """Test invalid quantity handling."""
    products = [
        (1, "Pen", 100.0, 10),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    inputs = iter(["1", "0", "1", "2", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        lambda cart, product_data, quantity: cart.append(product_data),
    )

    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: None,
    )

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Quantity must be greater than 0." in captured.out


def test_create_bill_product_not_found(monkeypatch, capsys):
    """Test handling of an invalid product ID."""
    products = [
        (1, "Pen", 100.0, 10),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    inputs = iter(["99", "2", "1", "1", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        lambda cart, product_data, quantity: cart.append(product_data),
    )

    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: None,
    )

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Product not found." in captured.out


def test_create_bill_insufficient_stock(monkeypatch, capsys):
    """Test handling of insufficient stock."""
    products = [
        (1, "Pen", 100.0, 3),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    inputs = iter(["1", "5", "1", "2", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        lambda cart, product_data, quantity: cart.append(product_data),
    )

    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: None,
    )

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Not enough stock. Available quantity: 3" in captured.out


def test_create_bill_invalid_input(monkeypatch, capsys):
    """Test ValueError handling."""
    products = [
        (1, "Pen", 100.0, 10),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    inputs = iter(["abc", "1", "2", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        lambda cart, product_data, quantity: cart.append(product_data),
    )

    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: None,
    )

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Please enter valid numeric values." in captured.out


def test_create_bill_add_another_product(monkeypatch, capsys):
    """Test adding multiple products to the same bill."""
    products = [
        (1, "Pen", 100.0, 10),
        (2, "Milk", 200.0, 10),
    ]

    monkeypatch.setattr("src.services.main.view_products", lambda: products)

    generated_bills = []

    monkeypatch.setattr(
        "src.services.main.add_item_to_cart",
        lambda cart, product_data, quantity: cart.append(product_data),
    )

    monkeypatch.setattr(
        "src.services.main.generate_bill",
        lambda cart: generated_bills.append(cart),
    )

    inputs = iter(["1", "2", "y", "2", "1", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.services.main import create_bill

    create_bill()

    captured = capsys.readouterr()

    assert "Added 2 x Pen to cart." in captured.out
    assert "Added 1 x Milk to cart." in captured.out
    assert len(generated_bills[0]) == 2
