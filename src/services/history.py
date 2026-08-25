import json
import sqlite3

from src.services import config
from src.services.logger_config import logger


def view_bill_history():
    """Fetch and display all past bills from the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        conn.close()

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

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        logger.error(f"Error viewing bill history: {e}")
