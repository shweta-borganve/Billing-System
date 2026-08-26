import json
import sqlite3

from src.database.db_operations import get_all_bills
from src.services import config
from src.services.logger_config import logger

# Compatibility constants for modules still referencing file paths
BILLS_FILE = "data/bills.json"
PRODUCTS_FILE = "data/products.json"


def load_data(filename):
    """Load data handler compatible with SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        if "bill" in filename.lower() or filename == BILLS_FILE:
            conn.close()
            return get_all_bills()

        elif "product" in filename.lower() or filename == PRODUCTS_FILE:
            cursor.execute("SELECT id, name, price, quantity FROM products")
            rows = cursor.fetchall()
            products = []
            for row in rows:
                p_id, name, price, quantity = row
                products.append(
                    {
                        "product_id": p_id,
                        "name": name,
                        "price": price,
                        "quantity": quantity,
                    }
                )
            conn.close()
            return products

        conn.close()
        return []
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logger.error(f"Error loading data for {filename}: {e}")
        return []


def save_data(filename, data):
    """Save data to SQLite database instead of dummy files."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        if "product" in filename.lower() or filename == PRODUCTS_FILE:
            cursor.execute("DELETE FROM products")
            for p in data:
                cursor.execute(
                    "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
                    (p["product_id"], p["name"], p["price"], p["quantity"]),
                )
            conn.commit()
            logger.info("Products successfully saved to SQLite database")

        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Error saving data for {filename}: {e}")


def save_bill_record(filename, items, total_amount, date):
    """Save a bill record safely to SQLite."""
    try:
        try:
            if isinstance(items, str):
                items = json.loads(items)
        except json.JSONDecodeError:
            pass

        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bills (date, total_amount, items) VALUES (?, ?, ?)",
            (date, total_amount, json.dumps(items)),
        )
        conn.commit()
        conn.close()
        logger.info("Bill saved successfully to SQLite database")

    except sqlite3.Error as e:
        logger.error(f"Error saving to database for {filename}: {e}")
