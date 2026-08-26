import sqlite3

from src.services import config
from src.services.logger_config import logger


def add_product():
    """Adds a new product to the database."""
    try:
feature/validation-and-logging
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

        name = input("Enter product name: ").strip()
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers for price and quantity.")
        return
main

    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            (name, price, quantity),
        )
        conn.commit()
        conn.close()
feature/validation-and-logging

        print("Product added successfully.")
        logger.info(f"Product added: {name} (ID: {product_id})")

    except ValueError:
        print(
            "Invalid input. Please enter correct numeric values for ID, price, and quantity."
        )
        logger.warning("Invalid input type while adding product.")

        print(f"Product '{name}' added successfully!")
main
    except sqlite3.Error as e:
        logger.error(f"Database error while adding product: {e}")
        print(f"Error adding product: {e}")


def view_products():
    """Displays all products in the database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, quantity FROM products")
        products = cursor.fetchall()
        conn.close()

        if not products:
            print("No products found.")
            return []

        formatted_products = []
        for p in products:
            prod = {"id": p[0], "name": p[1], "price": p[2], "quantity": p[3]}
            formatted_products.append(prod)
            print(f"ID: {p[0]} | Name: {p[1]} | Price: {p[2]} | Qty: {p[3]}")
        return formatted_products
    except sqlite3.Error as e:
        logger.error(f"Database error while viewing products: {e}")
        print(f"Error retrieving products: {e}")
        return []


def update_product():
    """Updates an existing product's details."""
    try:
        product_id = int(input("Enter product ID to update: "))
    except ValueError:
        print("Invalid product ID.")
        return

    try:
feature/validation-and-logging
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

        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            print(f"Product with ID {product_id} not found.")
main
            conn.close()
            return

        name = input("Enter new product name: ").strip()
        price = float(input("Enter new product price: "))
        quantity = int(input("Enter new product quantity: "))

        cursor.execute(
            "UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?",
            (name, price, quantity, product_id),
        )
        conn.commit()
        conn.close()
        print(f"Product {product_id} updated successfully!")
    except ValueError:
feature/validation-and-logging
        print("Invalid input. Please enter correct numeric values.")
        logger.warning("Invalid input while updating product.")

        print("Invalid numerical input.")
main
    except sqlite3.Error as e:
        logger.error(f"Database error while updating product: {e}")
        print(f"Error updating product: {e}")


def delete_product():
    """Deletes a product by ID."""
    try:
        product_id = int(input("Enter product ID to delete: "))
    except ValueError:
        print("Invalid product ID.")
        return

    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted > 0:
            print(f"Product {product_id} deleted successfully.")
        else:
            print(f"Product {product_id} not found.")
    except sqlite3.Error as e:
        logger.error(f"Database error while deleting product: {e}")
        print(f"Error deleting product: {e}")


def search_product():
    """Searches for products by name."""
    keyword = input("Enter search keyword: ").strip()
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price, quantity FROM products WHERE name LIKE ?",
            (f"%{keyword}%",),
        )
        products = cursor.fetchall()
        conn.close()

        if not products:
            print("No matching products found.")
            return []

        formatted = []
        for p in products:
            formatted.append(
                {"id": p[0], "name": p[1], "price": p[2], "quantity": p[3]}
            )
            print(f"ID: {p[0]} | Name: {p[1]} | Price: {p[2]} | Qty: {p[3]}")
        return formatted
    except sqlite3.Error as e:
        logger.error(f"Database error while searching product: {e}")
        print(f"Error searching product: {e}")
        return []
