import json
import sqlite3

from src.services import config
from src.services.logger_config import logger


def view_bill_history():
    """Fetch and display all past bills from the SQLite database."""
    try:
        with sqlite3.connect(config.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, total_amount, items FROM bills")
            bills = cursor.fetchall()

            if not bills:
                print("No bill history found.")
                return []

            formatted_bills = []
            for bill in bills:
                try:
                    items = json.loads(bill[3])
                except (json.JSONDecodeError, TypeError):
                    items = bill[3]

                bill_data = {
                    "id": bill[0],
                    "date": bill[1],
                    "total_amount": bill[2],
                    "items": items,
                }
                formatted_bills.append(bill_data)
                print(
                    f"Bill ID: {bill[0]} | Date: {bill[1]} | Total: {bill[2]} | Items: {items}"
                )
            return formatted_bills

    except sqlite3.Error as e:
        logger.error(f"Database error while fetching bill history: {e}")
        print(f"Error loading bill history: {e}")
        return []
