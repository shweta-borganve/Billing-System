import json
import sqlite3
from datetime import datetime, timezone

from src.billing.pdf_export import generate_pdf_receipt
from src.database.db_operations import update_product_quantity
from src.services import config
from src.services.file_handler import PRODUCTS_FILE, load_data
from src.services import config
from src.services.logger_config import logger


def check_low_stock_in_list(products, threshold=5):
    """Checks the current products array for items at or below the low stock threshold."""
    low_stock_items = []
    for product in products:
        if product.get("quantity", 0) <= threshold:
            low_stock_items.append((product.get("name"), product.get("quantity")))
    return low_stock_items


def generate_bill():
    products = load_data(PRODUCTS_FILE)

    if not products:
        print("No products available.")
        logger.warning("Bill generation attempted with no products.")
        return

    items = []
    total = 0

    while True:
        try:
            product_id = int(input("Enter Product ID (0 to finish): "))

            if product_id == 0:
                break

            quantity = int(input("Enter quantity: "))
            found = False

            for product in products:
                if int(product["product_id"]) == product_id:
                    found = True

                    if quantity <= 0:
                        print("Quantity must be greater than 0.")
                        logger.warning("Invalid quantity entered.")
                        break

                    if quantity > product["quantity"]:
                        print("Insufficient stock.")
                        logger.warning(f"Insufficient stock for product: {product_id}")
                        break

                    amount = product["price"] * quantity

                    item = {
                        "product_id": product["product_id"],
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": quantity,
                        "amount": amount,
                    }

                    items.append(item)
                    total += amount

                    new_qty = product["quantity"] - quantity
                    update_product_quantity(product["product_id"], quantity)
                    product["quantity"] = new_qty

                    print(f"Added {product['name']} to bill.")

                    if new_qty <= 5:
                        print(
                            f"ALERT: {product['name']} is now running low on stock ({new_qty} left)!"
                        )
                        logger.warning(
                            f"Low stock alert triggered for product {product['name']}: {new_qty} remaining."
                        )

                    break

            if not found:
                print("Product not found.")
                logger.warning(f"Product not found: {product_id}")

        except ValueError:
            print("Invalid input.")
            logger.warning("Invalid input during bill generation.")

def calculate_total(items):
    """Calculates the total amount for a list of bill items."""
    total = 0.0
    for item in items:
        total += item.get("price", 0.0) * item.get("quantity", 1)
    return total


def add_item_to_cart(cart, product, quantity=1):
    """Adds a product to the current billing cart or updates quantity if it exists."""
    for item in cart:
        if item.get("id") == product.get("id"):
            item["quantity"] += quantity
            return cart

    new_item = {
        "id": product.get("id"),
        "name": product.get("name"),
        "price": product.get("price"),
        "quantity": quantity,
    }
    cart.append(new_item)
    return cart


def remove_item_from_cart(cart, product_id):
    """Removes an item from the billing cart by product ID."""
    return [item for item in cart if item.get("id") != product_id]


def clear_cart():
    """Clears the current billing cart."""
    return []


def generate_bill(items):
    """Generates a bill, saves it to the database, and updates product stock."""
    if not items:
        print("No items provided for the bill.")
        return None

    total_amount = calculate_total(items)
    current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    items_json = json.dumps(items)

    try:
        conn = sqlite3.connect(config.DB_NAME)
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        # Ensure bills table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                items TEXT NOT NULL
            )
        """)

        # Insert bill record
        cursor.execute(
            "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
            (current_date, total_amount, items_json),
        )
        conn.commit()

        cursor.execute("SELECT last_insert_rowid()")
        bill_id = cursor.fetchone()[0]
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error while saving bill: {e}")
        logger.error(f"Database error saving bill: {e}")
        return

    print("\n===== BILL =====")
    print(f"Bill ID: {bill_id}")
    print(f"Date: {date_str}")

    for item in items:
        print(f"{item['name']} x {item['quantity']} = ₹{item['amount']:.2f}")

    print(f"Total: ₹{total:.2f}")
    logger.info(f"Bill generated successfully: {bill_id}")

    try:
        pdf_filename = f"bill_{bill_id}.pdf"
        generate_pdf_receipt(pdf_filename, bill_id, date_str, items, total)
        print(f"PDF receipt saved successfully as '{pdf_filename}'")
        logger.info(f"PDF receipt exported successfully: {pdf_filename}")
    except Exception as e:  # noqa: BLE001
        print(f"Error generating PDF receipt: {e}")
        logger.error(f"Error generating PDF receipt for bill {bill_id}: {e}")


def view_bill_history():
    """Fetch and display all past bills from the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        bills = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        logger.error(f"Error viewing bill history: {e}")
        return

    if not rows:
        print("No bill history available.")
        logger.warning("No bill history available to display.")
        return

    print("\n===== BILL HISTORY =====")
    for row in rows:
        bill_id, date, total_amount, items_data = row
        try:
            if isinstance(items_data, str):
                items_data = json.loads(items_data)
        except json.JSONDecodeError:
            items_data = []

        print(f"\nBill ID: {bill_id} | Date: {date}")
        print("-" * 35)
        for item in items_data:
            name = item.get("name", "Unknown")
            qty = item.get("quantity", 0)
            amount = item.get("amount", 0)
            print(f"  - {name} x {qty} = ₹{amount:.2f}")
        print(f"Total Amount: ₹{total_amount:.2f}")
        print("-" * 35)

    logger.info("Bill history viewed successfully.")
        if not bills:
            print("No bills found.")
            return []

        formatted_bills = []
        for bill in bills:
            bill_data = {
                "id": bill[0],
                "date": bill[1],
                "total_amount": bill[2],
                "items": json.loads(bill[3]),
            }
            formatted_bills.append(bill_data)
            print(f"Bill ID: {bill[0]} | Date: {bill[1]} | Total: {bill[2]}")
        return formatted_bills

    except sqlite3.Error as e:
        logger.error(f"Database error while viewing bills: {e}")
        print(f"Error retrieving bills: {e}")
        return []


def search_bill_by_id(bill_id):
    """Searches for a specific bill by its ID."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, date, total_amount, items FROM bills WHERE id = ?", (bill_id,)
        )
        bill = cursor.fetchone()
        conn.close()

        if not bill:
            print(f"Bill with ID {bill_id} not found.")
            return None

        bill_data = {
            "id": bill[0],
            "date": bill[1],
            "total_amount": bill[2],
            "items": json.loads(bill[3]),
        }
        return bill_data

    except sqlite3.Error as e:
        logger.error(f"Database error while searching bill: {e}")
        print(f"Error searching bill: {e}")
        return None


def delete_bill(bill_id):
    """Deletes a bill record by ID."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bills WHERE id = ?", (bill_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        conn.close()

        if deleted_rows > 0:
            print(f"Bill {bill_id} deleted successfully.")
            return True
        else:
            print(f"Bill {bill_id} not found for deletion.")
            return False

    except sqlite3.Error as e:
        logger.error(f"Database error while deleting bill: {e}")
        print(f"Error deleting bill: {e}")
        return False
