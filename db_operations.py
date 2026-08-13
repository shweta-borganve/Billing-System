import sqlite3
import json

def initialize_database():
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    
    # Create bills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def add_product(product_id, name, price, quantity):
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (product_id, name, price, quantity) VALUES (?, ?, ?, ?)",
                       (product_id, name, price, quantity))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Product ID already exists in database.")
    finally:
        conn.close()

def get_all_products():
    conn = sqlite3.connect("billing.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    products = []
    for row in rows:
        products.append({
            "product_id": row["product_id"],
            "name": row["name"],
            "price": row["price"],
            "quantity": row["quantity"]
        })
    conn.close()
    return products

def update_product_quantity(product_id, new_quantity):
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE product_id = ?", (new_quantity, product_id))
    conn.commit()
    conn.close()

def save_bill(items, total, timestamp):
    conn = sqlite3.connect("billing.db")
    cursor = conn.cursor()
    items_json = json.dumps(items)
    cursor.execute("INSERT INTO bills (items, total, timestamp) VALUES (?, ?, ?)",
                   (items_json, total, timestamp))
    conn.commit()
    conn.close()

def get_all_bills():
    """Retrieves all saved bills from the SQLite database."""
    try:
        conn = sqlite3.connect("billing.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bills")
        rows = cursor.fetchall()
        
        bills = []
        for row in rows:
            items_data = row["items"]
            
            # Safely parse items whether it's stored as a JSON string or double-encoded
            if isinstance(items_data, str):
                try:
                    items_data = json.loads(items_data)
                    if isinstance(items_data, str):
                        items_data = json.loads(items_data)
                except Exception:
                    items_data = []

            bills.append({
                "bill_id": row["id"],
                "date": row["timestamp"],
                "items": items_data if isinstance(items_data, list) else [],
                "total": row["total"]
            })
        conn.close()
        return bills
    except Exception as e:
        print(f"Error fetching bills: {e}")
        return []

if __name__ == "__main__":
    initialize_database()
    print("Database and tables created successfully!") 