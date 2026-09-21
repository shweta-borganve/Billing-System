import sqlite3

from src.auth.auth import login
from src.billing.analytics import generate_sales_report
from src.billing.billing import add_item_to_cart, generate_bill
from src.services.history import view_bill_history
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


def create_bill():
    """Creates a bill by selecting products and quantities."""
    cart = []

    while True:
        products = view_products()

        if not products:
            return

        try:
            product_id = int(input("Enter Product ID: "))
            quantity = int(input("Enter Quantity: "))

            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue

            product = next(
                (row for row in products if row[0] == product_id),
                None,
            )

            if product is None:
                print("Product not found.")
                continue

            if quantity > product[3]:
                print(f"Not enough stock. Available quantity: {product[3]}")
                continue

            product_data = {
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "quantity": quantity,
            }

            add_item_to_cart(cart, product_data, quantity)

            print(f"Added {quantity} x {product[1]} to cart.")

            another = input("Add another product? (y/n): ").strip().lower()

            if another != "y":
                break

        except ValueError:
            print("Please enter valid numeric values.")

    if cart:
        generate_bill(cart)


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
        print("10. Exit")

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
            create_bill()
        elif choice == "7":
            view_bill_history()
        elif choice == "8":
            generate_sales_report()
        elif choice == "9":
            check_and_display_low_stock()
        elif choice == "10":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":  # pragma: no cover
    main()
