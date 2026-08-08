from file_handler import load_data, BILLS_FILE
from logger_config import logger


def view_bill_history():
    bills = load_data(BILLS_FILE)

    if not bills:
        print("No bill history available.")
        logger.warning("Bill history requested but no bills found.")
        return

    print("\n===== Bill History =====")

    for bill in bills:
        print(f"\nBill ID: {bill['bill_id']}")
        print(f"Date: {bill['date']}")

        for item in bill["items"]:
            print(
                f"{item['name']} x {item['quantity']} "
                f"= ₹{item['amount']:.2f}"
            )

        print(f"Total: ₹{bill['total']:.2f}") 