import json
import sqlite3
from unittest.mock import patch

import pytest

from src.billing import billing
from src.services import config


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_db.db"
    original_db_name = config.DB_NAME
    config.DB_NAME = str(db_file)

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_details TEXT NOT NULL,
            total_amount REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    yield str(db_file)

    config.DB_NAME = original_db_name


def test_cart_operations():
    cart = []

    product1 = {
        "id": 1,
        "product_id": 1,
        "name": "Apple",
        "price": 10.0,
        "quantity": 5,
    }

    billing.add_item_to_cart(cart, product1, 2)

    assert len(cart) == 1
    assert cart[0]["quantity"] == 2

    billing.add_item_to_cart(cart, product1, 3)

    assert cart[0]["quantity"] == 5

    assert billing.calculate_total(cart) == 50.0

    low_stock = billing.check_low_stock_in_list(
        [product1],
        threshold=10,
    )

    assert len(low_stock) == 1

    cart = billing.remove_item_from_cart(cart, 1)

    assert len(cart) == 0

    assert billing.clear_cart() == []


def test_generate_bill_edge_cases(temp_db):
    # No products exist in the database.
    # generate_bill(None) should return None.
    assert billing.generate_bill(None) is None

    # Empty items list should also return None.
    assert billing.generate_bill([]) is None


def test_generate_bill_items_none_with_products(temp_db):
    # Add a product to the temporary database.
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, quantity) " "VALUES ('Pen', 5.0, 10)"
    )

    conn.commit()
    conn.close()

    # Enter 0 to finish the bill without adding any item.
    with patch("builtins.input", side_effect=["0"]):
        result = billing.generate_bill(None)

    # No items were added, so no bill should be generated.
    assert result is None


@patch("sqlite3.connect")
def test_generate_bill_database_error(mock_connect):
    mock_connect.side_effect = sqlite3.Error("DB Connection Error")

    with pytest.raises(sqlite3.Error):
        billing.generate_bill([{"id": 1, "price": 10, "quantity": 1}])


def test_bill_management_operations(temp_db):
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, quantity) " "VALUES ('Pen', 5.0, 10)"
    )

    conn.commit()
    conn.close()

    items = [
        {
            "id": 1,
            "name": "Pen",
            "price": 5.0,
            "quantity": 2,
        }
    ]

    total = billing.generate_bill(items)

    assert total == 10.0

    bills = billing.view_bills()

    assert len(bills) == 1

    bill_id = bills[0]["id"]

    assert len(billing.view_bill_history()) == 1

    searched = billing.search_bill_by_id(bill_id)

    assert searched is not None
    assert searched["id"] == bill_id

    assert billing.search_bill_by_id(9999) is None

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bills SET bill_details = 'invalid_json' " "WHERE bill_id = ?",
        (bill_id,),
    )

    conn.commit()
    conn.close()

    searched_bad_json = billing.search_bill_by_id(bill_id)

    assert searched_bad_json["items"] == []

    assert billing.delete_bill(bill_id) is True
    assert billing.delete_bill(9999) is False


def test_view_bills_and_history_json_error_lines_145_146(temp_db):
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bills "
        "(timestamp, total_amount, bill_details) "
        "VALUES ('2026-03-30', 100.0, 'bad_json')"
    )

    conn.commit()
    conn.close()

    with patch(
        "src.billing.billing.json.loads",
        side_effect=json.JSONDecodeError("Error", "doc", 0),
    ):
        bills = billing.view_bills()

        assert isinstance(bills, list)
        assert bills[0]["items"] == []

        history = billing.view_bill_history()

        assert isinstance(history, list)
        assert history[0]["items"] == []


def test_view_bills_and_history_exception_paths(temp_db):
    with patch(
        "src.billing.billing.sqlite3.connect",
        side_effect=sqlite3.Error("Fetch error"),
    ):
        assert billing.view_bills() == []
        assert billing.view_bill_history() == []


def test_search_and_delete_bill_exception_paths(temp_db):
    with patch(
        "src.billing.billing.sqlite3.connect",
        side_effect=sqlite3.Error("DB error"),
    ):
        assert billing.search_bill_by_id(1) is None
        assert billing.delete_bill(1) is False
