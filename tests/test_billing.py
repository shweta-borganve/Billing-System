import sqlite3
from unittest.mock import patch

import pytest

from src.billing import billing
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_billing.db"
    monkeypatch.setattr(config, "DB_NAME", str(db_file))
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items TEXT NOT NULL
        )
    """)
    cursor.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Pen', 10.0, 50)"
    )
    conn.commit()
    conn.close()
    return db_file


def test_calculate_total():
    items = [{"price": 10.0, "quantity": 2}, {"price": 5.0, "quantity": 3}]
    assert billing.calculate_total(items) == 35.0


def test_calculate_total_empty():
    assert billing.calculate_total([]) == 0.0


def test_add_item_to_cart_new():
    cart = []
    product = {"id": 1, "name": "Pen", "price": 10.0}
    updated_cart = billing.add_item_to_cart(cart, product, quantity=2)
    assert len(updated_cart) == 1
    assert updated_cart[0]["quantity"] == 2


def test_add_item_to_cart_existing():
    cart = [{"id": 1, "name": "Pen", "price": 10.0, "quantity": 2}]
    product = {"id": 1, "name": "Pen", "price": 10.0}
    updated_cart = billing.add_item_to_cart(cart, product, quantity=3)
    assert len(updated_cart) == 1
    assert updated_cart[0]["quantity"] == 5


def test_remove_item_from_cart():
    cart = [
        {"id": 1, "name": "Pen", "quantity": 2},
        {"id": 2, "name": "Notebook", "quantity": 1},
    ]
    updated_cart = billing.remove_item_from_cart(cart, 1)
    assert len(updated_cart) == 1
    assert updated_cart[0]["id"] == 2


def test_clear_cart():
    assert billing.clear_cart() == []


def test_generate_bill_empty():
    assert billing.generate_bill([]) is None


def test_generate_bill_success(temp_db):
    items = [{"id": 1, "name": "Pen", "price": 10.0, "quantity": 2}]
    total = billing.generate_bill(items)
    assert total == 20.0


def test_generate_bill_sqlite_error(temp_db):
    items = [{"id": 1, "name": "Pen", "price": 10.0, "quantity": 1}]
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
        pytest.raises(sqlite3.Error),
    ):
        billing.generate_bill(items)


def test_view_bills_empty(temp_db):
    with patch("builtins.print"):
        result = billing.view_bills()
        assert result == []


def test_view_bills_success(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        (
            "2026-06-06 12:00:00",
            20.0,
            '[{"id": 1, "name": "Pen", "price": 10.0, "quantity": 2}]',
        ),
    )
    conn.commit()
    conn.close()

    with patch("builtins.print"):
        bills = billing.view_bills()
        assert len(bills) == 1
        assert bills[0]["total_amount"] == 20.0


def test_view_bills_sqlite_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("View Error")),
        patch("builtins.print"),
    ):
        assert billing.view_bills() == []


def test_search_bill_by_id_success(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        (
            "2026-06-06 12:00:00",
            15.0,
            '[{"id": 1, "name": "Pen", "price": 15.0, "quantity": 1}]',
        ),
    )
    bill_id = cursor.lastrowid
    conn.commit()
    conn.close()

    bill = billing.search_bill_by_id(bill_id)
    assert bill is not None
    assert bill["total_amount"] == 15.0


def test_search_bill_by_id_not_found(temp_db):
    with patch("builtins.print"):
        assert billing.search_bill_by_id(999) is None


def test_search_bill_by_id_sqlite_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Search Error")),
        patch("builtins.print"),
    ):
        assert billing.search_bill_by_id(1) is None


def test_delete_bill_success(temp_db):
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
        ("2026-06-06 12:00:00", 10.0, "[]"),
    )
    bill_id = cursor.lastrowid
    conn.commit()
    conn.close()

    with patch("builtins.print"):
        assert billing.delete_bill(bill_id) is True


def test_delete_bill_not_found(temp_db):
    with patch("builtins.print"):
        assert billing.delete_bill(999) is False


def test_delete_bill_sqlite_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Delete Error")),
        patch("builtins.print"),
    ):
        assert billing.delete_bill(1) is False
