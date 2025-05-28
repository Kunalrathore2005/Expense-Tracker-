from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import csv
import os
from dateutil.parser import parse
import matplotlib

# Use a non-interactive backend to avoid display issues
matplotlib.use("Agg")

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_expenses()
        self.category_mappings = {}  # e.g., {"Dining": "Food"}

        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Input Frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add Expense", padding="5")
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Description
        ttk.Label(self.input_frame, text="Description:").grid(row=0, column=0, padx=5, pady=2)
        self.description_entry = ttk.Entry(self.input_frame)
        self.description_entry.grid(row=0, column=1, padx=5, pady=2)

        # Amount
        ttk.Label(self.input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=2)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=2)

        # Category
        ttk.Label(self.input_frame, text="Category:").grid(row=2, column=0, padx=5, pady=2)
        self.category_entry = ttk.Entry(self.input_frame)
        self.category_entry.grid(row=2, column=1, padx=5, pady=2)

        # Add Button
        ttk.Button(self.input_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=5)

        # Filter Frame
        self.filter_frame = ttk.LabelFrame(self.main_frame, text="Filter Expenses", padding="5")
        self.filter_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # Date Range
        ttk.Label(self.filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
        self.start_date_entry = ttk.Entry(self.filter_frame)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self.filter_frame, text="End Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=2)
        self.end_date_entry = ttk.Entry(self.filter_frame)
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=2)

        # Category Filter
        ttk.Label(self.filter_frame, text="Category:").grid(row=1, column=0, padx=5, pady=2)
        self.category_filter = ttk.Combobox(self.filter_frame, state="readonly")
        self.category_filter.grid(row=1, column=1, padx=5, pady=2)
        self.update_category_filter()

        # Filter and Clear Buttons
        ttk.Button(self.filter_frame, text="Apply Filter", command=self.view_expenses).grid(row=1, column=2, padx=5, pady=2)
        ttk.Button(self.filter_frame, text="Clear Filters", command=self.clear_filters).grid(row=1, column=3, padx=5, pady=2)

        # Display Frame
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Expenses", padding="5")
        self.display_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Treeview for expenses
        columns = ("Date", "Description", "Amount", "Category")
        self.tree = ttk.Treeview(self.display_frame, columns=columns, show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount ($)")
        self.tree.heading("Category", text="Category")
        self.tree.column("Date", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Amount", width=100)
        self.tree.column("Category", width=100)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Action Buttons
        ttk.Button(self.display_frame, text="Delete Selected", command=self.delete_expense).grid(row=1, column=0, pady=5)
        ttk.Button(self.display_frame, text="Download Expenses", command=self.download_expenses).grid(row=1, column=1, pady=5)
        ttk.Button(self.display_frame, text="Show Chart", command=self.show_expense_chart).grid(row=1, column=2, pady=5)
        self.chart_type = ttk.Combobox(self.display_frame, values=["Pie", "Bar"], state="readonly")
        self.chart_type.set("Pie")
        self.chart_type.grid(row=1, column=3, pady=5)

        # Category Combination Frame
        self.combine_frame = ttk.LabelFrame(self.main_frame, text="Combine Categories", padding="5")
        self.combine_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(self.combine_frame, text="Original Category:").grid(row=0, column=0, padx=5, pady=2)
        self.original_category_entry = ttk.Entry(self.combine_frame)
        self.original_category_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self.combine_frame, text="New Category:").grid(row=0, column=2, padx=5, pady=2)
        self.new_category_entry = ttk.Entry(self.combine_frame)
        self.new_category_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(self.combine_frame, text="Combine", command=self.combine_categories).grid(row=1, column=0, columnspan=4, pady=5)

        # Reset All Button
        ttk.Button(self.main_frame, text="Reset All Data", command=self.reset_all).grid(row=4, column=0, pady=5)

        # Initial Load
        self.view_expenses()

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load expenses. Starting with empty list.")
            return []

    def save_expenses(self):
        try:
            with open("expenses.json", "w") as f:
                json.dump(self.expenses, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save expenses: {str(e)}")

    def add_expense(self):
        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        if description and amount and category:
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                expense = {
                    "description": description,
                    "amount": amount,
                    "category": category,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.expenses.append(expense)
                self.save_expenses()
                self.update_category_filter()
                self.view_expenses()
                self.description_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.category_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive number for amount.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an expense to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete selected expense?"):
            index = int(self.tree.item(selected[0])["tags"][0])
            self.expenses.pop(index)
            self.save_expenses()
            self.update_category_filter()
            self.view_expenses()

    def view_expenses(self):
        self.tree.delete(*self.tree.get_children())
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        category = self.category_filter.get().strip()

        try:
            start = parse(start_date) if start_date else None
            end = parse(end_date) if end_date else None
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        for i, expense in enumerate(self.expenses):
            exp_date = parse(expense["date"])
            display_category = self.category_mappings.get(expense["category"], expense["category"])

            # Apply filters
            if start and exp_date < start:
                continue
            if end and exp_date > end:
                continue
            if category and display_category != category:
                continue

            self.tree.insert("", "end", values=(
                expense["date"],
                expense["description"],
                f"${expense['amount']:.2f}",
                display_category
            ), tags=(i,))

    def update_category_filter(self):
        categories = set(self.category_mappings.get(exp["category"], exp["category"]) for exp in self.expenses)
        categories = [""] + sorted(categories)  # Include empty option for no filter
        self.category_filter["values"] = categories

    def download_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses to download.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Expenses"
        )
        if file_path:
            try:
                # Apply filters to export
                filtered_expenses = self.get_filtered_expenses()
                if not filtered_expenses:
                    messagebox.showinfo("Info", "No expenses match the current filters.")
                    return
                if file_path.endswith(".csv"):
                    with open(file_path, "w", newline="") as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=["date", "description", "amount", "category"])
                        writer.writeheader()
                        for expense in filtered_expenses:
                            writer.writerow(expense)
                else:  # JSON
                    with open(file_path, "w") as jsonfile:
                        json.dump(filtered_expenses, jsonfile, indent=4)
                messagebox.showinfo("Success", "Expenses downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download expenses: {str(e)}")

    def get_filtered_expenses(self):
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        category = self.category_filter.get().strip()
        try:
            start = parse(start_date) if start_date else None
            end = parse(end_date) if end_date else None
        except ValueError:
            return self.expenses  # Return all if date parsing fails
        filtered = []
        for expense in self.expenses:
            exp_date = parse(expense["date"])
            display_category = self.category_mappings.get(expense["category"], expense["category"])
            if start and exp_date < start:
                continue
            if end and exp_date > end:
                continue
            if category and display_category != category:
                continue
            filtered.append(expense)
        return filtered

    def show_expense_chart(self):
        filtered_expenses = self.get_filtered_expenses()
        if not filtered_expenses:
            messagebox.showinfo("Info", "No expenses to display in chart.")
            return

        # Aggregate expenses by category
        category_totals = {}
        for expense in filtered_expenses:
            category = self.category_mappings.get(expense["category"], expense["category"])
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        if not labels:
            messagebox.showinfo("Info", "No data to display in chart.")
            return

        # Create chart window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Chart by Category")

        # Create chart
        fig, ax = plt.subplots(figsize=(8, 6))
        if self.chart_type.get() == "Pie":
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
            ax.axis("equal")
        else:  # Bar
            ax.bar(labels, sizes, color=plt.cm.Paired.colors[:len(labels)])
            ax.set_ylabel("Amount ($)")
            ax.set_xlabel("Category")
            plt.xticks(rotation=45, ha="right")

        ax.set_title("Expenses by Category")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def combine_categories(self):
        original = self.original_category_entry.get().strip()
        new = self.new_category_entry.get().strip()
        if original and new:
            if original in self.category_mappings.values():
                messagebox.showerror("Error", "Original category is already a mapped category.")
                return
            self.category_mappings[original] = new
            self.update_category_filter()
            self.view_expenses()
            self.original_category_entry.delete(0, tk.END)
            self.new_category_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Category '{original}' will be displayed as '{new}'.")
        else:
            messagebox.showerror("Error", "Both original and new category fields are required.")

    def clear_filters(self):
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.category_filter.set("")
        self.view_expenses()

    def reset_all(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all expenses?"):
            self.expenses = []
            self.save_expenses()
            self.update_category_filter()
            self.view_expenses()
            messagebox.showinfo("Success", "All expenses deleted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()