import unittest
from unittest.mock import patch

from src.services import main


class TestBillingSystem(unittest.TestCase):

    # Test failed login
    @patch("src.services.main.login", return_value=False)
    @patch("src.services.main.logger")
    def test_login_failed(self, mock_logger, mock_login):
        main.main()

        mock_login.assert_called_once()
        self.assertTrue(mock_login.return_value is False)

    # Test Add Product
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.add_product")
    @patch("builtins.input", side_effect=["1", "10"])
    def test_add_product(self, mock_input, mock_add_product, mock_login):
        main.main()
        mock_add_product.assert_called_once()

    # Test View Products
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.view_products")
    @patch("builtins.input", side_effect=["2", "10"])
    def test_view_products(self, mock_input, mock_view_products, mock_login):
        main.main()
        mock_view_products.assert_called_once()

    # Test Search Product
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.search_product")
    @patch("builtins.input", side_effect=["3", "10"])
    def test_search_product(self, mock_input, mock_search_product, mock_login):
        main.main()
        mock_search_product.assert_called_once()

    # Test Update Product
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.update_product")
    @patch("builtins.input", side_effect=["4", "10"])
    def test_update_product(self, mock_input, mock_update_product, mock_login):
        main.main()
        mock_update_product.assert_called_once()

    # Test Delete Product
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.delete_product")
    @patch("builtins.input", side_effect=["5", "10"])
    def test_delete_product(self, mock_input, mock_delete_product, mock_login):
        main.main()
        mock_delete_product.assert_called_once()

    # Test Generate Bill
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.generate_bill")
    @patch("builtins.input", side_effect=["6", "10"])
    def test_generate_bill(self, mock_input, mock_generate_bill, mock_login):
        main.main()
        mock_generate_bill.assert_called_once()

    # Test View Bill History
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.view_bill_history")
    @patch("builtins.input", side_effect=["7", "10"])
    def test_view_bill_history(self, mock_input, mock_view_bill_history, mock_login):
        main.main()
        mock_view_bill_history.assert_called_once()

    # Test Check Low Stock Alerts Option
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.sqlite3.connect")
    @patch("builtins.input", side_effect=["8", "10"])
    def test_check_low_stock_option(self, mock_input, mock_connect, mock_login):
        main.main()
        mock_connect.assert_called()

    # Test Sales Analytics & Reporting Option
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.generate_sales_report")
    @patch("builtins.input", side_effect=["9", "10"])
    def test_sales_analytics_option(
        self, mock_input, mock_generate_sales_report, mock_login
    ):
        main.main()
        mock_generate_sales_report.assert_called_once()

    # Test Invalid Choice
    @patch("src.services.main.login", return_value=True)
    @patch("src.services.main.logger")
    @patch("builtins.input", side_effect=["11", "10"])
    def test_invalid_choice(self, mock_input, mock_logger, mock_login):
        main.main()
        mock_logger.warning.assert_called_with("Invalid menu choice entered: 11")


if __name__ == "__main__":
    unittest.main()
