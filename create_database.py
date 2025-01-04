import sqlite3

def create_database():
    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    # Create Products Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   quantity INTEGER NOT NULL,
                   price REAL NOT NULL,
                   cost REAL NOT NULL,
                   restock_alert INTEGER NOT NULL
                   )
                   """)
    # Create Sales Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS sales (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   product_id INTEGER NOT NULL,
                   quantity_sold INTEGER NOT NULL,
                   total_sales REAL NOT NULL,
                   profit REAL NOT NULL,
                   date TEXT NOT NULL,
                   FOREIGN KEY (product_id) REFERENCES products (id)
                   )
                   """)
    conn.commit()
    conn.close()
    print("Datebase and tables created successfully.")

if __name__ == "__main__":
    create_database()