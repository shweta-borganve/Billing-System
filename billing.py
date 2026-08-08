from datetime import datetime

from file_handler import (
    load_data,
    save_data,
    PRODUCTS_FILE,
    BILLS_FILE
)
from logger_config import logger


def generate_bill():
    products = load_data(PRODUCTS_FILE)
    bills = load_data(BILLS_FILE)

    if not products:
        print("No products available.")
        logger.warning("Bill generation attempted with no products.")
        return

    items = []
    total = 0

    while True:
        try:
            product_id = int(input("Enter Product ID (0 to finish): "))

            if product_id == 0:
                break

            quantity = int(input("Enter quantity: "))

            found = False

            for product in products:

                if product["id"] == product_id:
                    found = True

                    if quantity <= 0:
                        print("Quantity must be greater than 0.")
                        logger.warning("Invalid quantity entered.")
                        continue

                    if quantity > product["quantity"]:
                        print("Insufficient stock.")
                        logger.warning(
                            f"Insufficient stock for product: {product_id}"
                        )
                        continue

                    amount = product["price"] * quantity

                    item = {
                        "product_id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": quantity,
                        "amount": amount
                    }

                    items.append(item)

                    product["quantity"] -= quantity
                    total += amount

                    print(f"Added {product['name']} to bill.")
                    break

            if not found:
                print("Product not found.")
                logger.warning(f"Product not found: {product_id}")

        except ValueError:
            print("Invalid input.")
            logger.warning("Invalid input during bill generation.")

    if not items:
        print("No items added to bill.")
        return

    bill = {
        "bill_id": len(bills) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": items,
        "total": total
    }

    bills.append(bill)

    save_data(PRODUCTS_FILE, products)
    save_data(BILLS_FILE, bills)

    print("\n===== BILL =====")
    print(f"Bill ID: {bill['bill_id']}")
    print(f"Date: {bill['date']}")

    for item in items:
        print(
            f"{item['name']} x {item['quantity']} = "
            f"₹{item['amount']:.2f}"
        )

    print(f"Total: ₹{total:.2f}")

    logger.info(f"Bill generated successfully: {bill['bill_id']}") 