# FinMatrics — Personal Expense Tracker & Budget Planner

A clean, console-based personal expense manager built in Python for our **Computational Thinking and Programming (2026CSAE100)** course at **Bennett University**.

---

## 📌 Overview
Most student expense trackers are either too basic or overcomplicated. We built **FinMatrics** to be simple, practical, and easy to use for students managing hostel and daily expenses.

It tracks daily income and expenses, calculates monthly summaries and category breakdowns, alerts you when you exceed your monthly budget, supports basic currency conversion (USD, EUR, GBP to INR), and lets you export monthly reports to text files.

---

## 👥 Team Members & Responsibilities

| Student Name | Enrollment No. | Contribution / Role |
|---|---|---|
| **Samriddhi Jain** | S26CSEU1985 | Menu navigation and input validation (dates, types, positive numbers) |
| **Pranjaldeep Kaur** | S26CSEU1934 | CSV storage engine (`load_transactions`, `save_transactions`, ID generation) |
| **Ashu Kumar** | S26CSEU1963 | Monthly summary engine, balance calculation, and category breakdown |
| **Ansh Vardhan** | S26CSEU1919 | Search & filter (category/date), monthly budget checker, and test cases |
| **Anant Gupta** | S26CSEU1940 | Report export to text file, currency converter, and system integration |

---

## 💡 Key Features

- **Add & View Transactions:** Record income and expenses with date, category, amount, currency, and description.
- **Search & Filter:** Find transactions by category, date, or type (income/expense).
- **Monthly Summary:** Calculates total income, total expenses, net balance, and finds your highest spending category.
- **Budget Alerts:** Set a monthly budget and instantly check if your expenses are within limits or overspent.
- **Currency Conversion:** Supports foreign currencies (USD, EUR, GBP, AED, CAD) with automatic conversion to base INR.
- **Delete Transactions:** Remove unwanted transactions by ID with confirmation.
- **Export Report:** Saves a clean, formatted monthly financial report (`monthly_report_YYYY-MM.txt`) for offline records.

---

## 🧠 Python Concepts Used

- **Data Structures:** Lists of dictionaries to store transaction records.
- **File Handling:** Using Python's built-in `csv` module to save and load data persistently, plus file writing for text reports.
- **Functions & Modularity:** Clean, single-purpose functions for each module.
- **Control Flow:** `while` loop for menu dispatch and `if-elif-else` branches for options and validation.
- **Exception Handling:** `try-except ValueError` blocks to reject invalid calendar dates and non-numeric amounts.
- **Standard Library:** Built entirely with Python standard libraries (`csv`, `datetime`, `pathlib`). Zero third-party packages needed.

---

## 📂 Project Structure

```text
├── main.py                 # Main console application
├── transactions.csv        # CSV file storing persistent records
├── test_expense_tracker.py # Automated test suite (8 tests)
└── README.md               # Project documentation
```

---

## 🚀 How to Run

Make sure you have Python 3 installed. No external packages are needed.

```bash
# Run the main program
python3 main.py

# Run the test cases
python3 test_expense_tracker.py
```
