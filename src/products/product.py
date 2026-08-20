import sqlite3

from src.services.config import DB_NAME
from src.services.logger_config import logger


def add_product():
    try:
        product_id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ").strip()

        # Validation: Ensure product name is not empty
        if not name:
            print("Product name cannot be empty.")
            logger.warning("Attempted to add product with empty name.")
            return

        price = float(input("Enter Product Price: "))
        # Validation: Price cannot be negative or zero
        if price <= 0:
            print("Price must be greater than 0.")
            logger.warning(f"Invalid price entered: {price}")
            return

        quantity = int(input("Enter Quantity: "))
        # Validation: Quantity cannot be negative
        if quantity < 0:
            print("Quantity cannot be negative.")
            logger.warning(f"Invalid quantity entered: {quantity}")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Check if product ID already exists
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if cursor.fetchone():
            print("Product ID already exists.")
            logger.warning(f"Duplicate product ID: {product_id}")
            conn.close()
            return

        # Insert new product into SQLite
        cursor.execute(
            "INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)",
            (product_id, name, price, quantity),
        )
        conn.commit()
        conn.close()

        print("Product added successfully.")
        logger.info(f"Product added: {name} (ID: {product_id})")

    except ValueError:
        print(
            "Invalid input. Please enter correct numeric values for ID, price, and quantity."
        )
        logger.warning("Invalid input type while adding product.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        logger.error(f"Database error while adding product: {e}")


def view_products():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, quantity FROM products")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No products available.")
            logger.warning("No products available to display.")
            return

        print("\n===== Products =====")
        for row in rows:
            p_id, name, price, quantity = row
            print(
                f"ID: {p_id} | "
                f"Name: {name} | "
                f"Price: ₹{price} | "
                f"Quantity: {quantity}"
            )
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        logger.error(f"Error viewing products: {e}")


def search_product():
    try:
        product_id = int(input("Enter Product ID to search: "))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price, quantity FROM products WHERE id = ?", (product_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            p_id, name, price, quantity = row
            print("\nProduct Found:")
            print(f"ID: {p_id} | Name: {name} | Price: ₹{price} | Quantity: {quantity}")
            logger.info(f"Product searched: {product_id}")
        else:
            print("Product not found.")
            logger.warning(f"Product not found: {product_id}")

    except ValueError:
        print("Invalid Product ID.")
        logger.warning("Invalid Product ID entered.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def update_product():
    try:
        product_id = int(input("Enter Product ID to update: "))

        name = input("Enter new name: ").strip()
        if not name:
            print("Product name cannot be empty.")
            logger.warning("Attempted to update product with empty name.")
            return

        price = float(input("Enter new price: "))
        if price <= 0:
            print("Price must be greater than 0.")
            logger.warning(f"Invalid price entered during update: {price}")
            return

        quantity = int(input("Enter new quantity: "))
        if quantity < 0:
            print("Quantity cannot be negative.")
            logger.warning(f"Invalid quantity entered during update: {quantity}")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            print("Product not found.")
            logger.close() if hasattr(logger, "close") else None
            conn.close()
            return

        cursor.execute(
            "UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?",
            (name, price, quantity, product_id),
        )
        conn.commit()
        conn.close()

        print("Product updated successfully.")
        logger.info(f"Product updated: {product_id}")

    except ValueError:
        print("Invalid input. Please enter correct numeric values.")
        logger.warning("Invalid input while updating product.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_product():
    try:
        product_id = int(input("Enter Product ID to delete: "))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            print("Product not found.")
            conn.close()
            return

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

        print("Product deleted successfully.")
        logger.info(f"Product deleted: {product_id}")

    except ValueError:
        print("Invalid Product ID.")
        logger.warning("Invalid Product ID entered.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
