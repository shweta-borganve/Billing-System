import json
import sqlite3


def get_all_bills():
    """Fetch all bills from the SQLite database."""
    try:
        conn = sqlite3.connect("billing.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, total_amount, items FROM bills")
        rows = cursor.fetchall()
        bills = []
        for row in rows:
            bill_id, date, total_amount, items_data = row
            try:
                if isinstance(items_data, str):
                    items_data = json.loads(items_data)
            except json.JSONDecodeError:
                items_data = []

            bills.append(
                {
                    "id": bill_id,
                    "date": date,
                    "total_amount": total_amount,
                    "items": items_data,
                }
            )
        conn.close()
        return bills
    except sqlite3.Error as e:
        print(f"Error fetching bills: {e}")
        return []


def update_product_quantity(product_id, quantity_sold):
    """Reduce product quantity in the database after a sale."""
    try:
        conn = sqlite3.connect("billing.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity_sold, product_id),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error updating product quantity: {e}")
