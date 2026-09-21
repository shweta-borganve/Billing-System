import json
import sqlite3

from src.services import config
from src.services.logger_config import logger


def execute_non_query(query, params=()):
    """Executes a write/update/create query against the database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error executing non-query: {e}")
        return
    finally:
        if conn:
            conn.close()


def execute_query(query, params=()):
    """Executes a read query against the database and returns all rows."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        logger.error(f"Error executing query: {e}")
        return []
    finally:
        if conn:
            conn.close()


def update_product_quantity(product_id, quantity_sold):
    """Reduce product quantity in the database after a sale."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE product_id = ?",
            (quantity_sold, product_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating product quantity: {e}")
        return
    finally:
        if conn:
            conn.close()


def get_all_bills():
    """Retrieves all bills from the database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bill_id, timestamp, total_amount, bill_details FROM bills"
        )
        rows = cursor.fetchall()

        bills = []
        for row in rows:
            bill_id, timestamp, total_amount, items_data = row
            try:
                if isinstance(items_data, str):
                    items_data = json.loads(items_data)
            except json.JSONDecodeError:
                items_data = []

            bills.append(
                {
                    "id": bill_id,
                    "date": timestamp,
                    "total_amount": total_amount,
                    "items": items_data,
                }
            )
        return bills
    except sqlite3.Error as e:
        logger.error(f"Error fetching bills: {e}")
        return []
    finally:
        if conn:
            conn.close()
