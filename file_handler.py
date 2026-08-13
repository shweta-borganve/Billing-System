import json
from db_operations import (
    get_all_products,
    get_all_bills,
    add_product as db_add_product,
    update_product_quantity as db_update_quantity,
    save_bill as db_save_bill
)
from logger_config import logger

PRODUCTS_FILE = "products"
BILLS_FILE = "bills"

def load_data(filename):
    """Loads products or bills from the SQLite database."""
    try:
        if "products" in str(filename):
            logger.info("Products loaded successfully from SQLite database")
            return get_all_products()
        elif "bills" in str(filename):
            logger.info("Bills loaded successfully from SQLite database")
            return get_all_bills()
        return []
    except Exception as e:
        logger.error(f"Error loading data for {filename}: {e}")
        return []

def save_data(filename, data):
    """Saves data into the SQLite database."""
    try:
        if "products" in str(filename):
            if isinstance(data, list) and len(data) > 0:
                new_item = data[-1]
                db_add_product(
                    str(new_item["product_id"]), 
                    new_item["name"], 
                    new_item["price"], 
                    new_item["quantity"]
                )
            logger.info("Product data saved to SQLite database")
        elif "bills" in str(filename):
            if isinstance(data, dict):
                items = data.get("items", [])
                # Ensure items is a list or properly loaded if it's already a string
                if isinstance(items, str):
                    try:
                        items = json.loads(items)
                    except:
                        pass
                
                db_save_bill(
                    json.dumps(items), 
                    data.get("total", 0.0), 
                    data.get("timestamp", data.get("date", ""))
                )
            logger.info("Bill saved successfully to SQLite database")
            
    except Exception as e:
        logger.error(f"Error saving to database for {filename}: {e}") 