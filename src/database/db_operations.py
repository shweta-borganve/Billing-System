import json
import sqlite3
from src.database.database import initialize_database  # Added export
from src.services import config
from src.services.logger_config import logger

def update_product_quantity(product_id, quantity_sold):
    """Reduce product quantity in the database after a sale."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
feature/pre-commit-hooks

        # Create products table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """
        )

        # Create bills table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                items TEXT NOT NULL
            )
        """
        )

        cursor.execute(query, params)

        cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity_sold, product_id),
        )
main
        conn.commit()
    except sqlite3.Error as e:  # pragma: no cover
        logger.error(f"Error updating product quantity: {e}")
    finally:
        if conn:
            conn.close()


def get_all_bills():
    """Retrieves all bills from the database."""
    conn = None
    rows = []
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "date": r[1],
                "total_amount": r[2],
                "items": json.loads(r[3]),
            }
            for r in rows
        ]
    except sqlite3.Error as e:  # pragma: no cover
        logger.error(f"Error fetching bills: {e}")
        return [
            {"id": r[0], "date": r[1], "total_amount": r[2], "items": r[3]}
            for r in rows
        ]
    finally:
        if conn:
            conn.close()