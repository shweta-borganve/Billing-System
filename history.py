from file_handler import BILLS_FILE, load_data
from logger_config import logger


def view_bill_history():
    bills = load_data(BILLS_FILE)

    if not bills:
        print("No bill history available.")
        logger.warning("Bill history requested but no bills found.")
        return

    print("\n===== Bill History =====")

    for bill in bills:
        print(f"\nBill ID: {bill.get('bill_id', 'N/A')}")
        print(f"Date: {bill.get('date', 'N/A')}")

        items = bill.get("items", [])
        for item in items:
            if isinstance(item, dict):
                name = item.get("name", "Unknown")
                qty = item.get("quantity", 0)
                amount = item.get("amount", 0.0)
                print(f"{name} x {qty} = ₹{amount:.2f}")
            else:
                # Fallback if an item was accidentally saved as a raw string
                print(f"- {item}")

        print(f"Total: ₹{bill.get('total', 0.0):.2f}") 