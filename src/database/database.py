import sqlite3

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
feature/mypy-type-checking
    """Creates the products and bills tables if they don't already exist."""

    """Initializes the required database tables."""
    conn = None
 main
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Create Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
feature/mypy-type-checking
                product_id TEXT PRIMARY KEY,

                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

feature/mypy-type-checking
        # Save (commit) the changes and close the connection
        conn.commit()
        conn.close()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        print(f"Error initializing database: {e}")


if __name__ == "__main__":  # pragma: no cover

        conn.commit()
        logger.info("Database and tables created successfully!")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_all_bills():
    """Retrieves all bill records from the database."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT bill_id, timestamp, total_amount, bill_details FROM bills"
        )
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        logger.error(f"Error fetching all bills: {e}")
        return []
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
main
    initialize_database()
