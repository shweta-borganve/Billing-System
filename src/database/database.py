import sqlite3

from src.services import config
from src.services.logger_config import logger


def get_connection():
    """Returns a database connection."""
    return sqlite3.connect(config.DB_NAME)


def initialize_database():
    """Initializes the database tables."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        print(f"Error initializing database: {e}")
