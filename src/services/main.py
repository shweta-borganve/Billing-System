import sqlite3

from src.products import product
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
    try:
        conn = sqlite3.connect(config.DB_NAME)
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
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database on startup: {e}")
        print("Database initialization error.")
        return

    while True:
        print("\n=== Billing System Menu ===")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Check Low Stock")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            product.add_product()
        elif choice == "2":
            product.view_products()
        elif choice == "3":
            product.update_product()
        elif choice == "4":
            product.delete_product()
        elif choice == "5":
            product.search_product()
        elif choice == "6":
            check_and_display_low_stock()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":  # pragma: no cover
    main()
