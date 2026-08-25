import json
import sqlite3

from src.services import config


def initialize_database():
    """Initialize the SQLite database and create required tables if they don't exist."""
    try:
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

        conn.commit()
        conn.close()
    except sqlite3.Error:  # pragma: no cover
        pass


def get_all_bills():
    """Fetch all bills from the SQLite database."""
    try:
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
