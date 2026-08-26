import sqlite3

from src.services import config
from src.services.logger_config import logger


def get_connection():
    """Returns a database connection."""
    return sqlite3.connect(config.DB_NAME)


def initialize_database():
    """Creates the products and bills tables if they don't already exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Create Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
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
        conn.close()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":  # pragma: no cover
    initialize_database()
