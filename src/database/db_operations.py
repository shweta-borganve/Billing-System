import sqlite3

from src.services import config
from src.services.logger_config import logger


def execute_non_query(query, params=()):
    """Executes INSERT, UPDATE, DELETE queries."""
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
main
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


def get_all_bills():
    """Retrieves all bills from the database."""
    conn = None
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        bills = [
            {"id": r[0], "date": r[1], "total_amount": r[2], "items": r[3]}
            for r in rows
        ]
        return bills
    except sqlite3.Error as e:
        logger.error(f"DB Error while fetching all bills: {e}")
        return []
    finally:
        if conn:
            conn.close()
