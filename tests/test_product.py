import sqlite3
from unittest.mock import MagicMock, patch

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
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    return db_file


def test_add_product_success(temp_db):
    inputs = iter(["1", "Apple", "50.0", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_empty_name(temp_db):
    inputs = iter(["1", "   ", "50.0", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_invalid_price_zero(temp_db):
    inputs = iter(["1", "Apple", "0", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_negative_quantity(temp_db):
    inputs = iter(["1", "Apple", "50.0", "-5"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_duplicate_id(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Milk', 30.0, 5)"
    )
    conn.commit()
    conn.close()

    inputs = iter(["1", "Apple", "50.0", "10"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_invalid_value(temp_db):
    inputs = iter(["abc"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.add_product()


def test_add_product_db_error(temp_db):
    inputs = iter(["1", "Apple", "50.0", "10"])
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
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Milk', 30.0, 5)"
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


def test_update_product_empty_name(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Bread', 20.0, 10)"
    )
    conn.commit()
    conn.close()

    inputs = iter(["1", "   "])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.update_product()


def test_update_product_invalid_price(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Bread', 20.0, 10)"
    )
    conn.commit()
    conn.close()

    inputs = iter(["1", "Whole Wheat", "0"])
    with patch("builtins.input", lambda _: next(inputs)), patch("builtins.print"):
        product.update_product()


def test_update_product_invalid_quantity(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Bread', 20.0, 10)"
    )
    conn.commit()
    conn.close()

    inputs = iter(["1", "Whole Wheat", "25.0", "-2"])
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


def test_update_product_execute_db_error(temp_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.execute.side_effect = [None, sqlite3.Error("Execute Error")]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    inputs = iter(["1", "New Bread", "25.0", "5"])
    with (
        patch("builtins.input", lambda _: next(inputs)),
        patch("sqlite3.connect", return_value=mock_conn),
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


def test_delete_product_execute_db_error(temp_db):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_cursor.execute.side_effect = [None, sqlite3.Error("Execute Error")]

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with (
        patch("builtins.input", return_value="1"),
        patch("sqlite3.connect", return_value=mock_conn),
        patch("builtins.print"),
    ):
        product.delete_product()


def test_search_product_success_name(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Apple Juice', 40.0, 10)"
    )
    conn.commit()
    conn.close()

    with patch("builtins.input", return_value="Apple"), patch("builtins.print"):
        res = product.search_product()
        assert len(res) == 1


def test_search_product_success_id(temp_db):
    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO products (id, name, price, quantity) VALUES (1, 'Apple Juice', 40.0, 10)"
    )
    conn.commit()
    conn.close()

    with patch("builtins.input", return_value="1"), patch("builtins.print"):
        res = product.search_product()
        assert len(res) == 1


def test_search_product_not_found(temp_db):
    with patch("builtins.input", return_value="Unknown"), patch("builtins.print"):
        res = product.search_product()
        assert res == []


def test_search_product_value_error(temp_db):
    with patch("builtins.input", return_value="Apple"), patch("builtins.print"):
        res = product.search_product()
        assert res == []


def test_search_product_db_error(temp_db):
    with (
        patch("builtins.input", return_value="1"),
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("builtins.print"),
    ):
        assert product.search_product() == []
