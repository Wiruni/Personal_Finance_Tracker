import json
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

transactions = []

def load_transactions():
    """Load transactions from a JSON file."""
    try:
        with open("transactions.json", "r") as file:
            data = json.load(file)
            global transactions
            transactions = data.get("transactions", [])
    except FileNotFoundError:
        transactions = []

def save_transactions():
    """Save transactions to a JSON file."""
    data = {"transactions": transactions}
    with open("transactions.json", "w") as file:
        json.dump(data, file)

def read_bulk_transactions_from_file(filename):
    """Read transactions from a file and add them to the current transactions."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            new_transactions = data.get("transactions", [])
            global transactions
            transactions.clear()
            transactions.extend(new_transactions)
        print("Bulk transactions read successfully and added.")
    except FileNotFoundError:
        print("File not found. No transactions were added.")

def add_transaction():
    """Add a new transaction."""
    amount = input("Enter the transaction amount: ")
    while not amount.replace(".", "", 1).isdigit():
        print("Invalid input. Please enter a valid amount.")
        amount = input("Enter the transaction amount: ")

    category = input("Enter the transaction category: ")

    type_ = input("Enter the transaction type (Income/Expense): ").lower()
    while type_ not in ["income", "expense"]:
        print("Invalid input. Please enter either 'Income' or 'Expense'.")
        type_ = input("Enter the transaction type (Income/Expense): ").lower()

    date = input("Enter the transaction date (YYYY-MM-DD): ")
    while len(date) != 10 or date[4] != "-" or date[7] != "-" or not date.replace("-", "").isdigit():
        print("Invalid input. Please enter a valid date (YYYY-MM-DD).")
        date = input("Enter the transaction date (YYYY-MM-DD): ")

    transactions.append({
        "amount": float(amount),
        "category": category,
        "type": type_.capitalize(),
        "date": date
    })
    print("Transaction added successfully.")

def view_transactions():
    """View all transactions in CLI with columns."""
    if not transactions:
        print("No transactions found.")
        return

    # Print header with column names
    print(f"{'Index':<6} {'Amount':<10} {'Category':<15} {'Type':<10} {'Date':<12}")
    print("-" * 60)

    # Print each transaction row with aligned columns
    for index, transaction in enumerate(transactions, start=1):
        print(f"{index:<6} Rs. {transaction['amount']:<8.2f} {transaction['category']:<15} {transaction['type']:<10} {transaction['date']:<12}")

def update_transaction():
    """Update a transaction."""
    view_transactions()
    if not transactions:
        print("No transactions to update.")
        return

    index = int(input("Enter the index of the transaction to update: "))
    if 1 <= index <= len(transactions):
        transaction = transactions[index - 1]
        transaction["amount"] = float(input("Enter the updated amount: "))
        transaction["category"] = input("Enter the updated category: ")
        transaction["type"] = input("Enter the updated type (Income/Expense): ").capitalize()
        transaction["date"] = input("Enter the updated date (YYYY-MM-DD): ")
        save_transactions()
        print("Transaction updated successfully.")
    else:
        print("Invalid index.")

def delete_transaction():
    """Delete a transaction."""
    view_transactions()
    if not transactions:
        print("No transactions to delete.")
        return

    index = int(input("Enter the index of the transaction to delete: "))
    if 1 <= index <= len(transactions):
        del transactions[index - 1]
        save_transactions()
        print("Transaction deleted successfully.")
    else:
        print("Invalid index.")

def display_summary():
    """Display summary of transactions."""
    if not transactions:
        print("No transactions to summarize.")
        return

    income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Income")
    expenses = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Expense")
    net_income = income - expenses

    print(f"Total Income: {income:.2f}")
    print(f"Total Expenses: {expenses:.2f}")
    print(f"Net Income: {net_income:.2f}")

def launch_gui():
    """Launch a simple GUI window."""
    root = tk.Tk()
    root.title("Personal Finance Tracker")

    root.geometry("400x500")

    def show_message(msg):
        messagebox.showinfo("Action", msg)

    tk.Label(root, text="Transaction Manager", font=("Helvetica", 18, "bold")).pack(pady=20)

    tk.Button(root, text="Add Transaction", width=30, command=open_add_transaction_window).pack(pady=5)
    tk.Button(root, text="View Transaction", width=30, command=open_view_transaction_window).pack(pady=5)
    tk.Button(root, text="Update Transaction", width=30, command=open_update_transaction_window).pack(pady=5)
    tk.Button(root, text="Delete Transaction", width=30, command=open_delete_transaction_window).pack(pady=5)
    tk.Button(root, text="Display Summary", width=30, command=open_display_summary_window).pack(pady=5)
    tk.Button(root, text="Read Bulk Transactions from File", width=30, command=open_read_bulk_transactions_window).pack(pady=5)
    tk.Button(root, text="Search Transactions", width=30, command=open_search_transaction_window).pack(pady=5)
    tk.Button(root, text="Sort Transactions (Ascending)", width=30, command=lambda: open_sorted_transactions_window("asc")).pack(pady=5)
    tk.Button(root, text="Sort Transactions (Descending)", width=30, command=lambda: open_sorted_transactions_window("desc")).pack(pady=5)
    tk.Button(root, text="Exit", width=30, command=lambda: exit_application(root), bg="red", fg="white").pack(pady=20)
    
    root.mainloop()

def open_add_transaction_window():
    add_win = tk.Toplevel()
    add_win.title("Add Transaction")
    add_win.geometry("300x300")

    tk.Label(add_win, text="Amount").pack()
    amount_entry = tk.Entry(add_win)
    amount_entry.pack()

    tk.Label(add_win, text="Category").pack()
    category_entry = tk.Entry(add_win)
    category_entry.pack()

    tk.Label(add_win, text="Type (Income/Expense)").pack()
    type_entry = tk.Entry(add_win)
    type_entry.pack()

    tk.Label(add_win, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(add_win)
    date_entry.pack()

    def save():
        amount = amount_entry.get()
        category = category_entry.get()
        type_ = type_entry.get().lower()
        date = date_entry.get()

        if not amount.replace(".", "", 1).isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return
        if type_ not in ["income", "expense"]:
            messagebox.showerror("Error", "Type must be 'Income' or 'Expense'")
            return
        if len(date) != 10 or date[4] != "-" or date[7] != "-" or not date.replace("-", "").isdigit():
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
            return

        transactions.append({
            "amount": float(amount),
            "category": category,
            "type": type_.capitalize(),
            "date": date
        })
        save_transactions()
        messagebox.showinfo("Success", "Transaction added successfully")
        add_win.destroy()

    tk.Button(add_win, text="Save", command=save).pack(pady=10)

def open_view_transaction_window():
    view_win = tk.Toplevel()
    view_win.title("All Transactions")
    view_win.geometry("600x400")

    tk.Label(view_win, text="All Transactions", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Frame for Treeview
    tree_frame = tk.Frame(view_win)
    tree_frame.pack(pady=10, fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(tree_frame)
    scrollbar.pack(side="right", fill="y")

    # Treeview Table
    columns = ("Index", "Amount", "Category", "Type", "Date")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Add data
    for idx, t in enumerate(transactions, start=1):
        tree.insert("", "end", values=(idx, t["amount"], t["category"], t["type"], t["date"]))

    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

def open_update_transaction_window():
    update_win = tk.Toplevel()
    update_win.title("Update Transaction")
    update_win.geometry("600x550")

    tk.Label(update_win, text="All Transactions", font=("Helvetica", 12, "bold")).pack(pady=5)

    # Treeview for tabular display
    tree_frame = tk.Frame(update_win)
    tree_frame.pack(pady=10)

    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
    tree.pack(side="left", fill="x")

    for col, heading in zip(columns, ["Index", "Amount", "Category", "Type", "Date"]):
        tree.heading(col, text=heading)
        tree.column(col, width=100)

    for idx, t in enumerate(transactions, start=1):
        tree.insert("", "end", values=(idx, t["amount"], t["category"], t["type"], t["date"]))

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Update form
    tk.Label(update_win, text="Enter Index to Update").pack()
    index_entry = tk.Entry(update_win)
    index_entry.pack()

    tk.Label(update_win, text="New Amount").pack()
    amount_entry = tk.Entry(update_win)
    amount_entry.pack()

    tk.Label(update_win, text="New Category").pack()
    category_entry = tk.Entry(update_win)
    category_entry.pack()

    tk.Label(update_win, text="New Type (Income/Expense)").pack()
    type_entry = tk.Entry(update_win)
    type_entry.pack()

    tk.Label(update_win, text="New Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(update_win)
    date_entry.pack()

    def update():
        idx = index_entry.get()
        if not idx.isdigit() or not (1 <= int(idx) <= len(transactions)):
            messagebox.showerror("Error", "Invalid index")
            return

        amount = amount_entry.get()
        category = category_entry.get()
        type_ = type_entry.get().lower()
        date = date_entry.get()

        if not amount.replace(".", "", 1).isdigit():
            messagebox.showerror("Error", "Invalid amount")
            return
        if type_ not in ["income", "expense"]:
            messagebox.showerror("Error", "Type must be 'Income' or 'Expense'")
            return
        if len(date) != 10 or date[4] != "-" or date[7] != "-" or not date.replace("-", "").isdigit():
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
            return

        transactions[int(idx) - 1] = {
            "amount": float(amount),
            "category": category,
            "type": type_.capitalize(),
            "date": date
        }
        save_transactions()
        messagebox.showinfo("Success", "Transaction updated successfully")
        update_win.destroy()

    tk.Button(update_win, text="Update", command=update).pack(pady=10)

def open_delete_transaction_window():
    del_win = tk.Toplevel()
    del_win.title("Delete Transaction")
    del_win.geometry("600x450")

    tk.Label(del_win, text="All Transactions", font=("Helvetica", 12, "bold")).pack(pady=5)

    # Table with scroll
    tree_frame = tk.Frame(del_win)
    tree_frame.pack(pady=10)

    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
    tree.pack(side="left", fill="x")

    for col, heading in zip(columns, ["Index", "Amount", "Category", "Type", "Date"]):
        tree.heading(col, text=heading)
        tree.column(col, width=100)

    for idx, t in enumerate(transactions, start=1):
        tree.insert("", "end", values=(idx, t["amount"], t["category"], t["type"], t["date"]))

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Entry for index to delete
    tk.Label(del_win, text="Enter Index to Delete").pack(pady=5)
    index_entry = tk.Entry(del_win)
    index_entry.pack()

    def delete():
        idx = index_entry.get()
        if not idx.isdigit() or not (1 <= int(idx) <= len(transactions)):
            messagebox.showerror("Error", "Invalid index")
            return
        transactions.pop(int(idx) - 1)
        save_transactions()
        messagebox.showinfo("Success", "Transaction deleted successfully")
        del_win.destroy()

    tk.Button(del_win, text="Delete", command=delete, bg="red", fg="white").pack(pady=10)

def open_display_summary_window():
    """Display a summary of all transactions in a GUI popup."""
    if not transactions:
        messagebox.showinfo("Summary", "No transactions to summarize.")
        return

    income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Income")
    expenses = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "Expense")
    net_income = income - expenses

    summary_win = tk.Toplevel()
    summary_win.title("Transaction Summary")
    summary_win.geometry("300x200")

    tk.Label(summary_win, text="Summary", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(summary_win, text=f"Total Income: Rs. {income:.2f}").pack(pady=5)
    tk.Label(summary_win, text=f"Total Expenses: Rs. {expenses:.2f}").pack(pady=5)
    tk.Label(summary_win, text=f"Net Income: Rs. {net_income:.2f}").pack(pady=5)


def open_read_bulk_transactions_window():
    bulk_win = tk.Toplevel()
    bulk_win.title("Load Bulk Transactions")
    bulk_win.geometry("300x150")

    def load_bulk():
        try:
            with open("transactions.json", "r") as file:
                data = json.load(file)
                if isinstance(data, dict) and "transactions" in data:
                    transactions.clear()
                    transactions.extend(data["transactions"])
                    save_transactions()
                    messagebox.showinfo("Success", "Transactions loaded successfully")
                    bulk_win.destroy()
                    show_transactions_from_file_window()
                    
                else:
                    messagebox.showerror("Error", "Invalid file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            bulk_win.destroy()

    tk.Label(bulk_win, text="Load all transactions from file?").pack(pady=10)
    tk.Button(bulk_win, text="Load", command=load_bulk).pack()

def show_transactions_from_file_window():
    view_win = tk.Toplevel()
    view_win.title("Transactions from File")
    view_win.geometry("550x400")

    tk.Label(view_win, text="Transactions from File", font=("Helvetica", 14, "bold")).pack(pady=10)

    columns = ("Index", "Amount", "Category", "Type", "Date")
    tree = ttk.Treeview(view_win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for idx, t in enumerate(transactions, start=1):
        tree.insert("", tk.END, values=(idx, t["amount"], t["category"], t["type"], t["date"]))

    tree.pack(fill="both", expand=True)

def open_search_transaction_window():
    search_win = tk.Toplevel()
    search_win.title("Search Transactions")
    search_win.geometry("400x400")

    tk.Label(search_win, text="Search Transactions", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Search field selection
    tk.Label(search_win, text="Select Search Field:").pack()
    field_var = tk.StringVar(value="category")
    search_options = ["category", "type", "date"]
    field_menu = tk.OptionMenu(search_win, field_var, *search_options)
    field_menu.pack(pady=5)

    # Search value entry
    tk.Label(search_win, text="Enter Search Value:").pack()
    search_entry = tk.Entry(search_win)
    search_entry.pack(pady=5)

    # Results area
    result_frame = tk.Frame(search_win)
    result_frame.pack(pady=10, fill="both", expand=True)

    result_text = tk.Text(result_frame, height=10, width=50)
    result_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
    scrollbar.pack(side="right", fill="y")
    result_text.config(yscrollcommand=scrollbar.set)

    def search(*args):
        field = field_var.get()
        value = search_entry.get().strip().lower()

        result_text.delete("1.0", tk.END)

        if not value:
            result_text.insert(tk.END, "Please enter a search value.")
            return

        matches = []
        for t in transactions:
            if field == "category" and t["category"].lower() == value:
                matches.append(t)
            elif field == "type" and t["type"].lower() == value:
                matches.append(t)
            elif field == "date" and t["date"] == value:
                matches.append(t)

        if matches:
            for idx, t in enumerate(matches, start=1):
                result_text.insert(tk.END,
                    f"{idx}. Amount: Rs. {t['amount']}, Category: {t['category']}, "
                    f"Type: {t['type']}, Date: {t['date']}\n\n")
        else:
            result_text.insert(tk.END, "No matching transactions found.")

    # Bind real-time search on entry change
    search_entry.bind("<KeyRelease>", search)

def open_sorted_transactions_window(order="asc"):
    sort_win = tk.Toplevel()
    sort_win.title(f"Transactions Sorted ({'Ascending' if order == 'asc' else 'Descending'})")
    sort_win.geometry("400x400")

    # Sort transactions
    sorted_txns = sorted(transactions, key=lambda x: x["amount"], reverse=(order == "desc"))

    # Create scrollable text area
    result_frame = tk.Frame(sort_win)
    result_frame.pack(pady=10, fill="both", expand=True)

    result_text = tk.Text(result_frame, height=20, width=50)
    result_text.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
    scrollbar.pack(side="right", fill="y")
    result_text.config(yscrollcommand=scrollbar.set)

    # Display sorted transactions
    if sorted_txns:
        for idx, t in enumerate(sorted_txns, start=1):
            result_text.insert(tk.END,
                f"{idx}. Amount: Rs. {t['amount']}, Category: {t['category']}, "
                f"Type: {t['type']}, Date: {t['date']}\n\n")
    else:
        result_text.insert(tk.END, "No transactions found.")

def exit_application(root):
    result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if result:
        root.destroy()

def main_menu():
    """Main menu for the application."""
    load_transactions()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read Bulk Transactions from File")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            read_bulk_transactions_from_file("transactions.json")
        elif choice == "7":
            save_transactions()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    load_transactions()

    print("\nLaunch Mode:")
    print("1. CLI Mode (Console)")
    print("2. GUI Mode (Window)")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        main_menu()
    elif choice == "2":
        launch_gui()
    else:
        print("Invalid choice. Exiting...")