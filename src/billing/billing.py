import json
import sqlite3
from datetime import datetime, timezone

from src.billing.pdf_export import generate_pdf_receipt
from src.services import config
from src.services.file_handler import PRODUCTS_FILE, load_data
from src.services.logger_config import logger


def calculate_total(items):
    """Calculates the total amount for a list of bill items."""
    total = 0.0
    for item in items:
        total += item.get("price", 0.0) * item.get("quantity", 1)
    return total


def add_item_to_cart(cart, product, quantity=1):
    """Adds a product to the current billing cart or updates quantity if it exists."""
    for item in cart:
        if item.get("id") == product.get("id") or item.get("product_id") == product.get(
            "product_id"
        ):
            item["quantity"] += quantity
            return cart

    new_item = {
        "id": product.get("id", product.get("product_id")),
        "product_id": product.get("product_id", product.get("id")),
        "name": product.get("name"),
        "price": product.get("price"),
        "quantity": quantity,
    }
    cart.append(new_item)
    return cart


def remove_item_from_cart(cart, product_id):
    """Removes an item from the billing cart by product ID."""
    return [
        item
        for item in cart
        if item.get("id") != product_id and item.get("product_id") != product_id
    ]


def clear_cart():
    """Clears the current billing cart."""
    return []


def check_low_stock_in_list(products, threshold=5):
    """Checks the current products array for items at or below the low stock threshold."""
    low_stock_items = []
    for product in products:
        if product.get("quantity", 0) <= threshold:
            low_stock_items.append((product.get("name"), product.get("quantity")))
    return low_stock_items


def generate_bill(items=None):
    """Generates a bill, saves it to the database, and updates product stock."""
    if items is None:
        products = load_data(PRODUCTS_FILE)
        if not products:
            print("No products available.")
            logger.warning("Bill generation attempted with no products.")
            return None
        items = []

    if not items:
        print("No items provided for the bill.")
        logger.warning("Bill generation attempted with no items.")
        return None

    total_amount = calculate_total(items)
    current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    items_json = json.dumps(items)

    try:
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

        cursor.execute("SELECT last_insert_rowid()")
        bill_id = cursor.fetchone()[0]

        # Update inventory stock
        for item in items:
            product_id = item.get("id", item.get("product_id"))
            qty_sold = item.get("quantity", 1)
            if product_id is not None:
                cursor.execute(
                    "UPDATE products SET quantity = quantity - ? WHERE id = ? OR product_id = ?",
                    (qty_sold, product_id, product_id),
                )

        conn.commit()
        conn.close()
        print(f"Bill generated successfully! Total Amount: {total_amount}")

        # Try generating PDF receipt if possible
        try:
            pdf_filename = f"bill_{bill_id}.pdf"
            generate_pdf_receipt(
                pdf_filename, bill_id, current_date, items, total_amount
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error generating PDF receipt: {e}")

        return total_amount

    except sqlite3.Error as e:
        logger.error(f"Database error during bill generation: {e}")
        print(f"Failed to generate bill due to database error: {e}")
        raise


def view_bills():
    """Retrieves and displays all generated bills from the database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        bills = cursor.fetchall()
        conn.close()

        if not bills:
            print("No bills found.")
            return []

        formatted_bills = []
        for bill in bills:
            try:
                items_parsed = json.loads(bill[3]) if bill[3] else []
            except json.JSONDecodeError:
                items_parsed = []

            bill_data = {
                "id": bill[0],
                "date": bill[1],
                "total_amount": bill[2],
                "items": items_parsed,
            }
            formatted_bills.append(bill_data)
        return formatted_bills

    except sqlite3.Error as e:
        logger.error(f"Database error while viewing bills: {e}")
        print(f"Error retrieving bills: {e}")
        return []


def view_bill_history():
    """Alias/wrapper for viewing bill history."""
    return view_bills()


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

        try:
            items_parsed = json.loads(bill[3]) if bill[3] else []
        except json.JSONDecodeError:
            items_parsed = []

        bill_data = {
            "id": bill[0],
            "date": bill[1],
            "total_amount": bill[2],
            "items": items_parsed,
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