import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from stock_management import (
    fetch_products,
    add_product,
    delete_product,
    edit_product,
    search_product_by_name,
    view_restock_alerts,
    export_products_to_csv
)

def open_stock_management():
    stock_window = tk.Toplevel()
    stock_window.title("Stock Management")
    stock_window.geometry("900x500")
    # Treeview for Displaying Products
    tree = ttk.Treeview(stock_window, columns=("ID", "Name", "Quantity", "Price", "Cost", "Restock Alert"), show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # Define Column Headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Cost", text="Cost")
    tree.heading("Restock Alert", text="Restock Alert")

    tree.column("ID", width=50)
    tree.column("Name", width=150)
    tree.column("Quantity", width=100)
    tree.column("Price", width=100)
    tree.column("Cost", width=100)
    tree.column("Restock Alert", width=100)
    # Refresh Table
    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        products = fetch_products()
        for product in products:
            tree.insert("", "end", values=product)
    refresh_table()

    # Add Product
    def open_add_product_window():
        add_window = tk.Toplevel(stock_window)
        add_window.title("Add Product")
        # Fields
        fields = [("Name", tk.StringVar()), ("Quantity", tk.IntVar()), ("Price", tk.DoubleVar()), ("Cost", tk.DoubleVar()), ("Restock Alert", tk.IntVar())]
        entries ={}
        for i, (label, var) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_window, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = var
        # Submit Button
        def submit_product():
            try:
                add_product(
                    name=entries["Name"].get(),
                    quantity=entries["Quantity"].get(),
                    price=entries["Price"].get(),
                    cost=entries["Cost"].get(),
                    restock_alert=entries["Restock Alert"].get()
                )
                add_window.destroy()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        tk.Button(add_window, text="Add Product", command=submit_product).grid(row=len(fields), column=0, columnspan=2, pady=10)
    # Search Product
    def open_search_product_window():
        search_window = tk.Toplevel(stock_window)
        search_window.title("Search Product")
        tk.Label(search_window, text="Product Name:").grid(row=0, column=0, padx=10, pady=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_window, textvariable=search_var)
        search_entry.grid(row=0, column=1, padx=10, pady=5)
        def search_product():
            products = search_product_by_name(search_var.get())
            for item in tree.get_children():
                tree.delete(item)
            for product in products:
                tree.insert("", "end", values=product)
            search_window.destroy()
        tk.Button(search_window, text="Search", command=search_product).grid(row=1, column=0, columnspan=2, pady=10)
    def open_edit_product_window():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected for editing.")
            return
        product_data = tree.item(selected_item)["values"]
        if not product_data:
            messagebox.showerror("Error", "Invalid product selection.")
            return
        edit_widow = tk.Toplevel(stock_window)
        edit_widow.title("Edit Product")
        fields = [("Name", tk.StringVar(value=product_data[1])),
                  ("Quantity", tk.IntVar(value=product_data[2])),
                  ("Price", tk.DoubleVar(value=product_data[3])),
                  ("Cost", tk.DoubleVar(value=product_data[4])),
                  ("Restock Alert", tk.IntVar(value=product_data[5]))]
        entries = {}
        for i, (label, var) in enumerate(fields):
            tk.Label(edit_widow, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_widow, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = var
        # Submit Button
        def submit_edit():
            try:
                edit_product(
                    product_id=product_data[0],
                    name=entries["Name"].get(),
                    quantity=entries["Quantity"].get(),
                    price=entries["Price"].get(),
                    cost=entries["Cost"].get(),
                    restock_alert=entries["Restock Alert"].get()
                )
                edit_widow.destroy()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        tk.Button(edit_widow, text="Save Changes", command=submit_edit).grid(row=len(fields), column=0, columnspan=2, pady=10)
    # View restocking Alerts
    def view_alerts():
        alerts = view_restock_alerts()
        if alerts:
            alert_message = "\n".join([f"Name: {alert[0]}, Quantity: {alert[1]}, Alert Level: {alert[2]}" for alert in alerts])
            messagebox.showinfo("Restocking", alert_message)
        else:
            messagebox.showinfo("Restocking Alerts", "No product below their restocking alert level.")
    # Export Products to csv
    def export_to_csv():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            export_products_to_csv(file_path)
    # Buttons
    button_frame = tk.Frame(stock_window)
    button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
    tk.Button(button_frame, text="Add Product", command=open_add_product_window, width=20).pack(pady=5)
    tk.Button(button_frame, text="Edit Product", command=open_edit_product_window, width=20).pack(pady=5)
    tk.Button(button_frame, text="Remove Product", command=lambda: delete_product(tree.item(tree.selection())["values"][0]) or refresh_table(), width=20).pack(pady=5)
    tk.Button(button_frame, text="Search Product", command=open_search_product_window, width=20).pack(pady=5)
    tk.Button(button_frame, text="View Restocking Alerts", command=view_alerts, width=20).pack(pady=5)
    tk.Button(button_frame, text="Export to CSV", command=export_to_csv, width=20).pack(pady=5)
    tk.Button(button_frame, text="Refresh", command=refresh_table, width=20).pack(pady=5)
