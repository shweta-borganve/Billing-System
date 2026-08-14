import sqlite3

from analytics import generate_sales_report
from auth import login
from billing import generate_bill
from config import DB_NAME
from db_operations import initialize_database
from history import view_bill_history
from logger_config import logger
from product import (
    add_product,
    delete_product,
    search_product,
    update_product,
    view_products,
)


def check_and_display_low_stock(threshold=5):
    """Checks the database for low stock items and displays a warning banner."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, quantity FROM products WHERE quantity <= ?", (threshold,)
        )
        low_stock_items = cursor.fetchall()
        conn.close()

        if low_stock_items:
            print("\n" + "=" * 50)
            print("WARNING: The following items are low in stock!")
            for name, qty in low_stock_items:
                print(f"   • {name}: only {qty} left!")
            print("=" * 50 + "\n")
            logger.warning(
                f"Low stock warning displayed for {len(low_stock_items)} item(s)."
            )
    except sqlite3.Error as e:
        logger.error(f"Database error checking low stock: {e}")


def main():
    # Ensure database and tables exist when the app starts
    initialize_database()

    print("===== Welcome to Billing System =====")

    if not login():
        return

    logger.info("Admin logged in successfully.")

    # Show low stock alerts automatically right after login/startup
    check_and_display_low_stock()

    while True:
        print("\n===== Billing System Menu =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Generate Bill")
        print("7. View Bill History")
        print("8. Check Low Stock Alerts")
        print("9. Sales Analytics & Reporting")
        print("10. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_product()
            elif choice == 2:
                view_products()
            elif choice == 3:
                search_product()
            elif choice == 4:
                update_product()
            elif choice == 5:
                delete_product()
            elif choice == 6:
                generate_bill()
            elif choice == 7:
                view_bill_history()
            elif choice == 8:
                check_and_display_low_stock()
            elif choice == 9:
                generate_sales_report()
            elif choice == 10:
                print("Thank you for using Billing System!")
                logger.info("Application exited.")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 10.")
                logger.warning(f"Invalid menu choice entered: {choice}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            logger.warning("Non-integer input entered for menu choice.")


if __name__ == "__main__":
    main()