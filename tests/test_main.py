import sqlite3
from unittest.mock import patch

from src.services import main


def test_check_and_display_low_stock_empty():
    with patch("sqlite3.connect") as mock_connect:
        mock_connect.return_value.cursor.return_value.fetchall.return_value = []
        main.check_and_display_low_stock()


def test_check_and_display_low_stock_with_items():
    with patch("sqlite3.connect") as mock_connect:
        mock_connect.return_value.cursor.return_value.fetchall.return_value = [
            ("Pen", 2)
        ]
        with patch("builtins.print"):
            main.check_and_display_low_stock()


def test_check_and_display_low_stock_db_error():
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("DB Error")),
        patch("src.services.main.logger") as mock_logger,
    ):
        main.check_and_display_low_stock()
        mock_logger.error.assert_called_once()


def test_main_menu_all_options():
    inputs = iter(["1", "2", "3", "4", "5", "6", "99", "0"])
    with (
        patch("builtins.input", lambda _: next(inputs)),
        patch("builtins.print"),
        patch("sqlite3.connect"),
        patch("src.products.product.add_product"),
        patch("src.products.product.view_products"),
        patch("src.products.product.update_product"),
        patch("src.products.product.delete_product"),
        patch("src.products.product.search_product"),
        patch("src.services.main.check_and_display_low_stock"),
    ):
        main.main()


def test_main_startup_database_error():
    with (
        patch("sqlite3.connect", side_effect=sqlite3.Error("Startup DB Error")),
        patch("builtins.print"),
    ):
        main.main()
