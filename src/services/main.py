import sqlite3

from src.auth.auth import login
from src.billing.analytics import generate_sales_report
from src.billing.billing import generate_bill, view_bill_history
from src.database.database import initialize_database
from src.products.product import (
    add_product,
    delete_product,
    search_product,
    update_product,
    view_products,
)
from src.services import config
from src.services.logger_config import logger


def check_and_display_low_stock():
    """Checks and displays items with low stock."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM products WHERE quantity < 5")
        low_items = cursor.fetchall()
        conn.close()
        if low_items:
            print("--- Low Stock Warnings ---")
            for name, qty in low_items:
                print(f"Alert: {name} is low on stock ({qty} remaining).")
    except sqlite3.Error as e:
        logger.error(f"Error checking low stock: {e}")


def main():
    """Main application loop."""
    if not login():
        print("Authentication failed. Exiting...")
        return

    initialize_database()

    while True:
        print("\n=== Billing System Menu ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Generate Bill")
        print("7. View Bill History")
        print("8. Generate Sales Report")
        print("9. Check Low Stock")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            generate_bill()
        elif choice == "7":
            view_bill_history()
        elif choice == "8":
            generate_sales_report()
        elif choice == "9":
            check_and_display_low_stock()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":  # pragma: no cover
    main()
