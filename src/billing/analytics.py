import json
import sqlite3
from collections import Counter

from src.services import config
from src.services.logger_config import logger


def generate_sales_report():
    """Calculates and displays sales analytics and reporting from the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()

        # Fetch total amounts and items from the SQLite bills table
        cursor.execute("SELECT total_amount, items FROM bills")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("\nNo sales data available to generate a report.")
            logger.warning("Sales report attempted with no bill history.")
            return

        total_revenue = 0.0
        total_bills = len(rows)
        item_sales_count = Counter()

        for total_amount, items_data in rows:
            total_revenue += total_amount
            try:
                if isinstance(items_data, str):
                    items_data = json.loads(items_data)

                for item in items_data:
                    name = item.get("name", "Unknown")
                    qty = item.get("quantity", 0)
                    item_sales_count[name] += qty
            except json.JSONDecodeError:
                continue

        print("\n" + "=" * 45)
        print("===== SALES ANALYTICS REPORT ===== ")
        print("=" * 45)
        print(f"Total Revenue      : ₹{total_revenue:.2f}")
        print(f"Total Transactions : {total_bills}")
        print("-" * 45)

        print("Best-Selling Products:")
        if item_sales_count:
            for name, qty in item_sales_count.most_common(5):
                print(f"   • {name}: {qty} unit(s) sold")
        else:
            print("   • No item data recorded.")

        print("=" * 45 + "\n")
        logger.info("Sales report generated successfully.")

    except sqlite3.Error as e:
        print(f"Database error while generating report: {e}")
        logger.error(f"Database error in sales report: {e}")
