import sqlite3
import os
from tkinter import messagebox
from datetime import datetime
# Absolute database path
db_path = os.path.abspath("shop.db")

def add_sales_to_db(product_id, quantity_sold):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Check if the product exists