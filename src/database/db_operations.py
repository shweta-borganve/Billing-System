import sqlite3

from src.services import config
from src.services import config
from src.services.logger_config import logger


def execute_non_query(query, params=()):
    """Executes INSERT, UPDATE, DELETE queries."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products ( 
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

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
    except sqlite3.Error:  # pragma: no cover
        pass
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


def get_all_bills():
    """Retrieves all bills from the database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r[0],
                "date": r[1],
                "total_amount": r[2],
                "items": json.loads(r[3]),
            }
            for r in rows
        ]
    except sqlite3.Error:  # pragma: no cover
        bills = [
            {"id": r[0], "date": r[1], "total_amount": r[2], "items": r[3]}
            for r in rows
        ]
        return bills
    except sqlite3.Error as e:
        logger.error(f"DB Error while fetching all bills: {e}")
        return []


def update_product_quantity(product_id, quantity_sold):
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
    except sqlite3.Error:  # pragma: no cover
        pass
    finally:
        if conn:
            conn.close()
