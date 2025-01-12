import tkinter as tk
from tkinter import ttk
from threading import Thread
import asyncio
from datetime import datetime

# Mock database for menu items and orders
menu_items = {
    "Pizza": 10.99,
    "Burger": 7.99,
    "Pasta": 8.99,
    "Salad": 5.99,
    "Soda": 1.99
}

orders = []  # List to store orders

# Discount and Tax Settings
discount_rate = 0.1  # 10% discount
tax_rate = 0.07  # 7% tax

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Order Management System")
        self.root.geometry("1000x700")

        self.active_frame = None
        self.show_main_menu()

    def show_main_menu(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tk.Frame(self.root)
        self.active_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(self.active_frame, text="Welcome to Restaurant Order Management System", font=("Helvetica", 18, "bold"), bg="blue", fg="white")
        header.pack(fill=tk.X)

        menu_button = tk.Button(self.active_frame, text="Menu Management", font=("Helvetica", 14), command=self.show_menu_management)
        menu_button.pack(pady=20)

        order_button = tk.Button(self.active_frame, text="Order Management", font=("Helvetica", 14), command=self.show_order_management)
        order_button.pack(pady=20)

        footer = tk.Label(self.active_frame, text="AZD", font=("Helvetica", 10, "italic"), bg="blue", fg="white")
        footer.pack(side=tk.BOTTOM, fill=tk.X)

    def show_menu_management(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tk.Frame(self.root, bg="lightgray")
        self.active_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(self.active_frame, text="Menu Management", font=("Helvetica", 16, "bold"), bg="blue", fg="white")
        header.pack(fill=tk.X)

        tk.Label(self.active_frame, text="Menu Items", font=("Helvetica", 14), bg="lightgray").pack(anchor="w", padx=10)

        self.menu_listbox = tk.Listbox(self.active_frame, font=("Helvetica", 12), height=10)
        for item, price in menu_items.items():
            self.menu_listbox.insert(tk.END, f"{item} - ${price:.2f}")
        self.menu_listbox.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.active_frame, text="New Item Name:", font=("Helvetica", 12), bg="lightgray").pack(anchor="w", padx=10)
        self.new_item_name_entry = tk.Entry(self.active_frame, font=("Helvetica", 12))
        self.new_item_name_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.active_frame, text="New Item Price:", font=("Helvetica", 12), bg="lightgray").pack(anchor="w", padx=10)
        self.new_item_price_entry = tk.Entry(self.active_frame, font=("Helvetica", 12))
        self.new_item_price_entry.pack(fill=tk.X, padx=10, pady=5)

        add_item_button = tk.Button(self.active_frame, text="Add Item", font=("Helvetica", 12), command=self.add_menu_item)
        add_item_button.pack(pady=10)

        back_button = tk.Button(self.active_frame, text="Back to Main Menu", font=("Helvetica", 12), command=self.show_main_menu)
        back_button.pack(pady=10)

    def add_menu_item(self):
        """Add a new item to the menu."""
        item_name = self.new_item_name_entry.get().strip()
        item_price = self.new_item_price_entry.get().strip()

        if not item_name or not item_price:
            return

        if not item_price.replace('.', '', 1).isdigit():
            return

        menu_items[item_name] = float(item_price)

        self.show_order_management()

    def show_order_management(self):
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = tk.Frame(self.root, bg="white")
        self.active_frame.pack(fill=tk.BOTH, expand=True)

        header = tk.Label(self.active_frame, text="Order Management", font=("Helvetica", 16, "bold"), bg="blue", fg="white")
        header.pack(fill=tk.X)

        # Order entry
        order_entry_frame = tk.Frame(self.active_frame)
        order_entry_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(order_entry_frame, text="Customer Name:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.customer_name_entry = tk.Entry(order_entry_frame, font=("Helvetica", 12))
        self.customer_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        back_button = tk.Button(order_entry_frame, text="Back to Main Menu", font=("Helvetica", 12), command=self.show_main_menu)
        back_button.pack(side=tk.RIGHT, padx=5)

        tk.Label(self.active_frame, text="Select Menu Items:", font=("Helvetica", 12)).pack(anchor="w", padx=10, pady=5)

        self.items_frame = tk.Frame(self.active_frame)
        self.items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.render_menu_items()

        # Footer for billing and grand total
        footer_frame = tk.Frame(self.active_frame, bg="white")
        footer_frame.pack(fill=tk.X, pady=10, padx=10)

        place_order_button = tk.Button(footer_frame, text="Place Order", font=("Helvetica", 12), command=self.add_order)
        place_order_button.pack(side=tk.LEFT)

        generate_bill_button = tk.Button(footer_frame, text="Generate Bill", font=("Helvetica", 12), command=self.generate_bill)
        generate_bill_button.pack(side=tk.LEFT, padx=5)

        reset_button = tk.Button(footer_frame, text="X", font=("Helvetica", 12), command=self.reset_orders)
        reset_button.pack(side=tk.LEFT, padx=5)

        self.grand_total_label = tk.Label(footer_frame, text="Grand Total: $0.00", font=("Helvetica", 14, "bold"), bg="white", fg="green")
        self.grand_total_label.pack(side=tk.RIGHT)

        # Order list
        self.order_tree = ttk.Treeview(self.active_frame, columns=("Customer", "Item", "Quantity", "Total"), show="headings")
        self.order_tree.heading("Customer", text="Customer")
        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Quantity", text="Quantity")
        self.order_tree.heading("Total", text="Total")
        self.order_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Billing section
        self.bill_text = tk.Text(self.active_frame, font=("Helvetica", 12), height=10, state="normal", bg="lightyellow")
        self.bill_text.insert(tk.END, "Bill Details will be displayed here\n")
        self.bill_text.pack(fill=tk.X, padx=10, pady=5)
        self.bill_text.config(state="disabled")

    def render_menu_items(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        num_columns = 5
        current_row = 0
        current_column = 0

        self.menu_item_checkboxes = {}
        self.menu_item_quantities = {}

        for item, price in menu_items.items():
            frame = tk.Frame(self.items_frame, relief=tk.GROOVE, borderwidth=1)
            frame.grid(row=current_row, column=current_column, padx=5, pady=5, sticky="nsew")

            var = tk.IntVar()
            cb = tk.Checkbutton(frame, text=f"{item} - ${price:.2f}", variable=var, font=("Helvetica", 12), anchor="w")
            cb.pack(anchor="w", padx=5, pady=5)
            self.menu_item_checkboxes[item] = var

            qty_entry = tk.Entry(frame, font=("Helvetica", 10))
            qty_entry.insert(0, "1")
            qty_entry.pack(anchor="w", padx=5, pady=2)
            self.menu_item_quantities[item] = qty_entry

            current_column += 1
            if current_column == num_columns:
                current_column = 0
                current_row += 1

    def add_order(self):
        """Add a new order based on selected items and quantities."""
        customer_name = self.customer_name_entry.get().strip()

        if not customer_name:
            return

        for item, var in self.menu_item_checkboxes.items():
            if var.get() == 1:
                quantity = self.menu_item_quantities[item].get().strip()
                if not quantity.isdigit() or int(quantity) <= 0:
                    continue

                quantity = int(quantity)
                total = menu_items[item] * quantity

                orders.append({"customer": customer_name, "item": item, "quantity": quantity, "total": total})
                self.order_tree.insert("", tk.END, values=(customer_name, item, quantity, f"${total:.2f}"))

        self.update_grand_total()

    def update_grand_total(self):
        """Calculate and display the grand total for all orders."""
        grand_total = sum(order["total"] for order in orders)
        self.grand_total_label.config(text=f"Grand Total: ${grand_total:.2f}")

    def reset_orders(self):
        """Reset all orders and clear the interface for a new session."""
        global orders
        orders = []
        self.order_tree.delete(*self.order_tree.get_children())
        self.update_grand_total()
        self.bill_text.config(state="normal")
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, "Bill Details will be displayed here\n")
        self.bill_text.config(state="disabled")
        self.customer_name_entry.delete(0, tk.END)

    def generate_bill(self):
        """Generate the detailed bill for all orders."""
        self.bill_text.config(state="normal")
        self.bill_text.delete(1.0, tk.END)
        total_cost = sum(order["total"] for order in orders)
        discount = total_cost * discount_rate
        tax = (total_cost - discount) * tax_rate

        bill_details = "Bill Details:\n\n"
        for order in orders:
            bill_details += f"{order['quantity']} x {order['item']} @ ${menu_items[order['item']]:.2f} = ${order['total']:.2f}\n"
        bill_details += f"Discount: -${discount:.2f}\n"
        bill_details += f"Tax: +${tax:.2f}\n\n"
        bill_details += f"Grand Total: ${total_cost:.2f}\n"

        self.bill_text.insert(tk.END, bill_details)
        self.bill_text.config(state="disabled")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
