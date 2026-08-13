from db_operations import initialize_database
from auth import login
from product import add_product, view_products, search_product, update_product, delete_product
from billing import generate_bill
from history import view_bill_history
from logger_config import logger


def main():
    # Ensure database and tables exist when the app starts
    initialize_database()

    print("===== Welcome to Billing System =====")

    if not login():
        return

    logger.info("Admin logged in successfully.")

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

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_product()
            elif choice == 2:
                view_products()
            elif choice == 3:
                search_product()
            elif choice == 4:
                update_product()
            elif choice == 5:
                delete_product()
            elif choice == 6:
                generate_bill()
            elif choice == 7:
                view_bill_history()
            elif choice == 8:
                print("Thank you for using Billing System!")
                logger.info("Application exited.")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 8.")
                logger.warning(f"Invalid menu choice entered: {choice}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            logger.warning("Non-integer input entered for menu choice.")


if __name__ == "__main__":
    main() 