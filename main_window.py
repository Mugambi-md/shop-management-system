import tkinter as tk
from stock_management_gui import open_stock_management

def open_main_window():
    root = tk.Tk()
    root.title("Shop Management System")
    root.geometry("400x300")

    tk.Button(root, text="Manage Stock", command=open_stock_management).pack(padx=20)

    root.mainloop()

if __name__ == "__main__":
    open_main_window()