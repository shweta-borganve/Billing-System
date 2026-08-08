from file_handler import load_data, save_data, PRODUCTS_FILE
from logger_config import logger


def add_product():
    products = load_data(PRODUCTS_FILE)

    try:
        product_id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        quantity = int(input("Enter Quantity: "))

        for product in products:
            if product["id"] == product_id:
                print("Product ID already exists.")
                logger.warning(f"Duplicate product ID: {product_id}")
                return

        product = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity
        }

        products.append(product)
        save_data(PRODUCTS_FILE, products)

        print("Product added successfully.")
        logger.info(f"Product added: {name}")

    except ValueError:
        print("Invalid input.")
        logger.warning("Invalid input while adding product.")


def view_products():
    products = load_data(PRODUCTS_FILE)

    if not products:
        print("No products available.")
        logger.warning("No products available to display.")
        return

    print("\n===== Products =====")

    for product in products:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ₹{product['price']} | "
            f"Quantity: {product['quantity']}"
        )


def search_product():
    products = load_data(PRODUCTS_FILE)

    try:
        product_id = int(input("Enter Product ID to search: "))

        for product in products:
            if product["id"] == product_id:
                print("\nProduct Found:")
                print(product)
                logger.info(f"Product searched: {product_id}")
                return

        print("Product not found.")
        logger.warning(f"Product not found: {product_id}")

    except ValueError:
        print("Invalid Product ID.")
        logger.warning("Invalid Product ID entered.")


def update_product():
    products = load_data(PRODUCTS_FILE)

    try:
        product_id = int(input("Enter Product ID to update: "))

        for product in products:
            if product["id"] == product_id:

                product["name"] = input("Enter new name: ")
                product["price"] = float(input("Enter new price: "))
                product["quantity"] = int(input("Enter new quantity: "))

                save_data(PRODUCTS_FILE, products)

                print("Product updated successfully.")
                logger.info(f"Product updated: {product_id}")
                return

        print("Product not found.")
        logger.warning(f"Product not found for update: {product_id}")

    except ValueError:
        print("Invalid input.")
        logger.warning("Invalid input while updating product.")


def delete_product():
    products = load_data(PRODUCTS_FILE)

    try:
        product_id = int(input("Enter Product ID to delete: "))

        for product in products:
            if product["id"] == product_id:

                products.remove(product)
                save_data(PRODUCTS_FILE, products)

                print("Product deleted successfully.")
                logger.info(f"Product deleted: {product_id}")
                return

        print("Product not found.")
        logger.warning(f"Product not found for deletion: {product_id}")

    except ValueError:
        print("Invalid Product ID.")
        logger.warning("Invalid Product ID entered.") 