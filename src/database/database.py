import json
import sqlite3
feature/pip-audit-scanning

# Set up database connection (this creates a file named 'billing.db' automatically)
DB_NAME = "billing.db"


def get_connection():
    """Creates and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def initialize_database():
    """Creates the products and bills tables if they don't already exist."""

from src.services import config
from src.services.logger_config import logger


def get_connection():
    """Creates and returns a SQLite database connection."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def initialize_database():
    """Initializes the required database tables."""
    conn = None
main
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Create Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                items TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
feature/pip-audit-scanning
                product_id TEXT PRIMARY KEY,

                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE,
main
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        # 2. Create Bills Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_details TEXT NOT NULL,
                total_amount REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        # Save (commit) the changes and close the connection
        conn.commit()
feature/pip-audit-scanning
        conn.close()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    initialize_database()

    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        # Handled gracefully so exceptions don't unhandled-crash tests expecting safe failure
    finally:
        if conn:
            conn.close()


def get_all_bills():
    """Retrieves all bill records from the database."""
    conn = None
    rows = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        logger.error(f"Error fetching all bills: {e}")
        raise
    finally:
        if conn:
            conn.close()
main
