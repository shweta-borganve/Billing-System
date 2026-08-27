import json
import sqlite3
from typing import Any

from src.services import config
from src.services.logger_config import logger


def initialize_database() -> None:
    """Initialize the SQLite database and create required tables if they don't exist."""


def execute_non_query(query, params=()):
    """Executes a write/update/create query against the database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products ( 
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        # Create bills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                items TEXT NOT NULL
            )
        """)

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


def get_all_bills() -> list[dict[str, Any]]:
    """Fetch all bills from the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bill_id, timestamp, total_amount, bill_details FROM bills"
        )
        rows = cursor.fetchall()

feature/mypy-type-checking
        bills: list[dict[str, Any]] = []
        for row in rows:
            bill_id, date, total_amount, items_data = row

        bills = []
        for row in rows:
            bill_id, timestamp, total_amount, items_data = row
main
            try:
                if isinstance(items_data, str):
                    items_data = json.loads(items_data)
            except json.JSONDecodeError:
                items_data = []

            bills.append(
                {
                    "id": bill_id,
feature/mypy-type-checking
                    "date": date,

                    "date": timestamp,
main
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


def update_product_quantity(product_id: int, quantity_sold: int) -> None:
    """Reduce product quantity in the database after a sale."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity_sold, product_id),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Error updating product quantity: {e}")
        print(f"Error updating product quantity: {e}")
