import sqlite3
from unittest.mock import patch

import pytest

from src.products import product
from src.services import config


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_product.db"
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
    conn.commit()
    conn.close()
    return db_file


def test_add_product_success(temp_db):
    inputs = iter(["Apple", "50.0", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_invalid_price(temp_db):
    inputs = iter(["Apple", "invalid_price"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_db_error(temp_db):
    inputs = iter(["Apple", "50.0", "10"])
    with (
        patch("builtins.input", lambda _: next(inputs)),
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        product.add_product()


def test_view_products_empty(temp_db):
    with patch("builtins.print"):
        res = product.view_products()
        assert res == []


def test_view_products_with_data(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (name, price, quantity) VALUES ('Milk', 30.0, 5)"
    )
    conn.commit()
    conn.close()
    with patch("builtins.print"):
        res = product.view_products()
        assert len(res) == 1


def test_view_products_db_error(temp_db):
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        assert product.view_products() == []


def test_update_product_success(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Bread', 20.0, 10)"
    )
    conn.commit()
    conn.close()

    inputs = iter(["1", "Whole Wheat", "25.0", "15"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.update_product()


def test_update_product_invalid_id(temp_db):
    with patch("builtins.input", return_value="abc"), patch("builtins.print"):
        product.update_product()


def test_update_product_not_found(temp_db):
    inputs = iter(["999"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.update_product()


def test_update_product_value_error(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Bread', 20.0, 10)"
    )
    conn.commit()
    conn.close()
    inputs = iter(["1", "Bad Name", "not_a_float", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.update_product()


def test_update_product_db_error(temp_db):
    with (
        patch("builtins.input", return_value="1"),
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        product.update_product()


def test_delete_product_success(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Butter', 50.0, 2)"
    )
    conn.commit()
    conn.close()

    with patch("builtins.input", return_value="1"), patch("builtins.print"):
        product.delete_product()


def test_delete_product_invalid_id(temp_db):
    with patch("builtins.input", return_value="abc"), patch("builtins.print"):
        product.delete_product()


def test_delete_product_not_found(temp_db):
    with patch("builtins.input", return_value="999"), patch("builtins.print"):
        product.delete_product()


def test_delete_product_db_error(temp_db):
    with (
        patch("builtins.input", return_value="1"),
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        product.delete_product()


def test_search_product_success(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (name, price, quantity) VALUES ('Apple Juice', 40.0, 10)"
    )
    conn.commit()
    conn.close()

    with patch("builtins.input", return_value="Apple"), patch("builtins.print"):
        res = product.search_product()
        assert len(res) == 1


def test_search_product_not_found(temp_db):
    with patch("builtins.input", return_value="Unknown"), patch("builtins.print"):
        res = product.search_product()
        assert res == []


def test_search_product_db_error(temp_db):
    with (
        patch("builtins.input", return_value="Apple"),
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        assert product.search_product() == []
