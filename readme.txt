Expense Tracker Application
Overview
The Expense Tracker Application is a Python-based desktop application built with Tkinter for managing personal expenses. It allows users to add, delete, filter, and visualize expenses, with features like category combination, data persistence, and export capabilities. The application provides a user-friendly interface with a tabular display, charts, and robust error handling, making it suitable for tracking daily expenditures.
Features

Add Expenses: Record expenses with description, amount, category, and timestamp.
Delete Expenses: Remove selected expenses with confirmation.
Filter Expenses: Filter by date range and category for targeted views.
Category Combination: Map similar categories (e.g., "Dining" to "Food") for unified reporting.
Data Visualization: Display expenses by category using pie or bar charts.
Export Data: Download expenses as CSV or JSON, with support for filtered data.
Persistence: Save expenses to expenses.json for data retention across sessions.
Tabular Display: View expenses in a sortable table with scrollbars using ttk.Treeview.
Reset Data: Clear all expenses with confirmation.
Modern UI: Organized layout with ttk widgets for a polished look.

Requirements

Python: Version 3.8 or higher (tested with 3.13).
Libraries:
tkinter (included with standard Python)
matplotlib (for charts)
python-dateutil (for date parsing)
csv (included with standard Python)
json (included with standard Python)



Installation

Install Python:

Download and install Python from python.org or your package manager.
Ensure Python is added to your system PATH.


Install Dependencies:Run the following command to install required libraries:
pip install matplotlib python-dateutil


Download the Code:

Clone or download the project repository.
Save the main script as expense_tracker.py.



Usage

Run the Application:Navigate to the project directory and run:
python expense_tracker.py


Interface Overview:

Add Expense: Enter description, amount, and category; click "Add Expense".
Filter Expenses: Specify start/end dates (YYYY-MM-DD) and/or select a category; click "Apply Filter".
Clear Filters: Reset filters to view all expenses.
Delete Expense: Select an expense in the table and click "Delete Selected".
View Chart: Choose "Pie" or "Bar" and click "Show Chart" to visualize expenses by category.
Download Expenses: Click "Download Expenses" to export as CSV or JSON.
Combine Categories: Enter original and new category names; click "Combine" to map them.
Reset All: Click "Reset All Data" to delete all expenses (with confirmation).


Data Storage:

Expenses are saved to expenses.json in the working directory.
Ensure write permissions in the directory to avoid file I/O errors.



Example

Add an Expense:
Description: "Lunch", Amount: "15.50", Category: "Dining"
Click "Add Expense" to record.


Combine Categories:
Original: "Dining", New: "Food"
Click "Combine" to display "Dining" as "Food" in views and charts.


Filter by Date:
Start Date: "2025-05-01", End Date: "2025-05-31"
Click "Apply Filter" to show May 2025 expenses.


Export:
Click "Download Expenses", select CSV, and save to expenses.csv.



File Structure

expense_tracker.py: Main application script.
expenses.json: Auto-generated file for storing expenses (created on first save).
README.md: This documentation file.

Notes

Date Format: Use YYYY-MM-DD for date filters (e.g., 2025-05-24). Flexible formats are supported via python-dateutil.
Category Mappings: Applied dynamically for display; original categories are preserved in expenses.json.
Charts: Pie and bar charts reflect filtered data. Requires matplotlib.
Error Handling: Includes validation for amounts, dates, and file operations, with user-friendly messages.
Scalability: Suitable for moderate datasets. For large datasets, consider a database like SQLite.

Troubleshooting

File I/O Errors: Ensure write permissions for expenses.json. Check the working directory.
Missing Libraries: Install matplotlib and python-dateutil as described.
Invalid Date Format: Use YYYY-MM-DD or a parseable format (e.g., 2025/05/24).
Chart Display Issues: Ensure matplotlib is installed correctly. The Agg backend is used to avoid display conflicts.

Future Enhancements

Add expense editing functionality.
Implement table sorting by columns (e.g., date, amount).
Add summary statistics (e.g., total spent, average per category).
Support additional chart types or time-based trends.
Integrate a database for large-scale data management.

License
This project is open-source and available under the MIT License.
Acknowledgments
Built with Python, Tkinter, and Matplotlib. Special thanks to the open-source community for providing robust libraries.

Last updated: May 24, 2025
