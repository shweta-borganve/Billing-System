import json
import sqlite3

from src.services.config import DB_NAME  # <-- Updated to modular path


def initialize_database():
    """Initialize the SQLite database and create required tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)  # <-- Updated to use DB_NAME
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

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")


def get_all_bills():
    """Fetch all bills from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)  # <-- Updated to use DB_NAME
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        bills = []
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
        conn.close()
        return bills
    except sqlite3.Error as e:
        print(f"Error fetching bills: {e}")
        return []


def update_product_quantity(product_id, quantity_sold):
    """Reduce product quantity in the database after a sale."""
    try:
        conn = sqlite3.connect(DB_NAME)  # <-- Updated to use DB_NAME
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity_sold, product_id),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error updating product quantity: {e}")