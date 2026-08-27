import json
import sqlite3
from typing import Any

from src.services import config
from src.services.logger_config import logger


def initialize_database() -> None:
    """Initialize the SQLite database and create required tables if they don't exist."""


def execute_non_query(query, params=()):
    """Executes INSERT, UPDATE, DELETE queries."""
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
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"DB Error in execute_non_query: {e}")
        raise


def execute_query(query, params=()):
    """Executes SELECT queries and returns results."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        logger.error(f"DB Error in execute_query: {e}")
        raise


def get_all_bills() -> list[dict[str, Any]]:
    """Fetch all bills from the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()

        bills: list[dict[str, Any]] = []
        for row in rows:
            bill_id, date, total_amount, items_data = row
            try:
                if isinstance(items_data, str):
                    items_data = json.loads(items_data)
            except json.JSONDecodeError:
                items_data = []

            bills.append(
                {
                    "id": bill_id,
                    "date": date,
                    "total_amount": total_amount,
                    "items": items_data,
                }
            )
        return bills
    except sqlite3.Error as e:
        logger.error(f"DB Error while fetching all bills: {e}")
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
