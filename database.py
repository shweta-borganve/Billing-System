import sqlite3
import logging

# Set up database connection (this creates a file named 'billing.db' automatically)
DB_NAME = "billing.db"

def get_connection():
    """Creates and returns a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def initialize_database():
    """Creates the products and bills tables if they don't already exist."""
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

if __name__ == "__main__":
    initialize_database() 