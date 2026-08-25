import json
import sqlite3
from datetime import datetime, timezone

from src.billing.pdf_export import generate_pdf_receipt
from src.database.db_operations import update_product_quantity
from src.services import config
from src.services.file_handler import PRODUCTS_FILE, load_data
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

    if not items:
        print("No items added to bill.")
        return

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
            (date_str, total, json.dumps(items)),
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
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
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
