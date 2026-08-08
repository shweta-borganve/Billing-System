from auth import login
from billing import generate_bill
from history import view_bill_history
from logger_config import logger
from product import (
    add_product,
    delete_product,
    search_product,
    update_product,
    view_products,
)


def main():

    logger.info("Billing System started.")

    print("===== Welcome to Billing System =====")

    if not login():
        print("Access Denied!")
        logger.warning("User failed authentication.")
        return

    while True:

        print("\n===== Billing System Menu =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Generate Bill")
        print("7. View Bill History")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            search_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            generate_bill()

        elif choice == "7":
            view_bill_history()

        elif choice == "8":
            logger.info("Billing System closed.")
            print("Thank you for using Billing System!")
            break

        else:
            print("Invalid choice!")
            logger.warning("Invalid menu choice entered.")


if __name__ == "__main__":
    main()
