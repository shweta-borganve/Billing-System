import json
import sqlite3

from db_operations import get_all_bills
from logger_config import logger

# Compatibility constants for modules still referencing file paths
BILLS_FILE = "data/bills.json"
PRODUCTS_FILE = "data/products.json"


def load_data(filename):
    """Load data handler compatible with SQLite or fallbacks."""
    try:
        if "bill" in filename.lower() or filename == BILLS_FILE:
            return get_all_bills()
        return []
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logger.error(f"Error loading data for {filename}: {e}")
        return []


def save_data(filename, data):
    """Compatibility wrapper for saving data."""
    logger.info(f"save_data called for {filename} (handled via SQLite)")


def save_bill_record(filename, items, total_amount, date):
    """Save a bill record safely."""
    try:
        try:
            items = json.loads(items)
        except json.JSONDecodeError:
            pass

        conn = sqlite3.connect("billing.db")
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
