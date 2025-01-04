import sqlite3
import os
from tkinter import messagebox
import csv
# Absolute database path
db_path = os.path.abspath("shop.db")
def fetch_products():
    """Fetch all products fron database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, price, cost, restock_alert FROM products")
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return []
    finally:
        conn.close()

def add_product(name, quantity, price, cost, restock_alert):
    """Add a new product to the database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO products (name, quantity, price, cost, restock_alert)
                       VALUES (?, ?, ?, ?, ?)""", (name, quantity, price, cost, restock_alert))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        conn.close()

def delete_product(product_id):
    """Remove a product from database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        messagebox.showinfo("Success!", "Product deleted successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        conn.close()

def edit_product(product_id, name=None, quantity=None, price=None, cost=None, restock_alert=None):
    """Edit an existing product in the database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Update only provided fields
        if name:
            cursor.execute("UPDATE products SET name=? WHERE id=?", (name, product_id))
        if quantity:
            cursor.execute("UPDATE products SET quantity=? WHERE id=?", (quantity, product_id))
        if price:
            cursor.execute("UPDATE products SET price=? WHERE id=?", (price, product_id))
        if cost:
            cursor.execute("UPDATE products SET cost=? WHERE id=?", (cost, product_id))
        if restock_alert:
            cursor.execute("UPDATE products SET restock_alert=? WHERE id=?", (restock_alert, product_id))
        conn.commit()
        messagebox.showinfo("Success!", "Product updated successfully!.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        conn.close()

def search_product_by_name(product_name):
    """Search for products by name."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + product_name + '%',))
        products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return []
    finally:
        conn.close()

def view_restock_alerts():
    """View products below their restocking alert level."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, restock_alert FROM products WHERE quantity<restock_alert")
        low_stock_products = cursor.fetchall()
        return low_stock_products
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return []
    finally:
        conn.close()

def export_products_to_csv(filename):
    """Export products data to a csv file."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, price, cost, restock_alert FROM products")
        products = cursor.fetchall()
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Name", "Quantity", "Price", "Cost", "Restock Alert"])
            writer.writerows(products)
        messagebox.showinfo("Success", f"Product exported to {filename} successfully!.")
    except sqlite3.Error as e:
        messagebox.showinfo("Database Error", f"Error: {e}")
    finally:
        conn.close()