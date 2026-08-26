import sqlite3

from src.services import config


def initialize_database():
    """Initialize the SQLite database and create required tables if they don't exist."""
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

        conn.commit()
        conn.close()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
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
