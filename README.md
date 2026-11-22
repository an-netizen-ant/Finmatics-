# FinMatrics — Personal Expense Tracker & Budget Planner

A console-based personal finance manager built in Python for our **Computational Thinking and Programming (2026CSAE100)** course at **Bennett University**.

---

## 📌 Overview
Most basic student expense trackers just add numbers and print them out. We wanted to make something actually useful for students managing their monthly pocket money and hostel expenses. 

**FinMatrics** lets you track daily income and expenses, checks your monthly budget, identifies which category you spent the most on, and gives basic advice on how to save or invest your remaining balance. It also has basic typo-handling so minor spelling mistakes don't crash the program.

---

## 👥 Team Members & Responsibilities

| Student Name | Enrollment No. | Contribution / Role |
|---|---|---|
| **Samriddhi Jain** | S26CSEU1985 | Menu design, input validation, and 50/30/20 rule calculation |
| **Pranjaldeep Kaur** | S26CSEU1934 | CSV file storage (`transactions.csv`) and currency conversion |
| **Ashu Kumar** | S26CSEU1963 | Monthly summaries, category grouping, and SIP investment calculations |
| **Ansh Vardhan** | S26CSEU1919 | Recurring subscriptions audit, anomaly detection, and test cases |
| **Anant Gupta** | S26CSEU1940 | Text report export, typo assistance, and code integration |

---

## 💡 Key Features

- **Add & View Transactions:** Log expenses and income with date, category, and currency (defaults to INR ₹, but supports USD, EUR, GBP, etc.).
- **Monthly Summary:** Calculates total income, expenses, net savings, and points out your highest spending category.
- **Budget Alerts:** Warns you when your spending crosses 85% of your set budget or if you overspend.
- **50/30/20 Financial Health Score:** Checks whether your spending roughly aligns with 50% Needs, 30% Wants, and 20% Savings.
- **Savings Advice (SIP & Emergency Fund):** Gives simple suggestions on how to split leftover money into an emergency buffer and long-term savings.
- **Typo Tolerance:** If you make a small typo (like typing `sumary` instead of `3`, or `usdd` for currency), the program catches it and continues without crashing.
- **Export Report:** Saves a clean text summary (`monthly_report_YYYY-MM.txt`) to keep offline records.

---

## 🧠 Python Concepts Used

- **Data Structures:** Lists and Dictionaries for holding and grouping transaction records; Sets for fast category lookup.
- **File Handling:** Using Python's built-in `csv` module to save and load data persistently.
- **Functions & Modularity:** Program is broken down into small, single-purpose functions.
- **Control Flow:** `while` loops for the interactive menu and `if-elif-else` conditions for validations.
- **Error Handling:** `try-except` blocks to handle invalid dates, non-numeric amounts, or corrupted rows safely.
- **Standard Libraries:** `datetime` (date checking), `math` (compounding math), and `difflib` (typo auto-correction).

---

## 📂 Project Structure

```text
├── main.py                 # Main program (run this)
├── transactions.csv        # CSV file storing all transaction records
├── test_expense_tracker.py # Test file verifying the core functions
└── README.md               # Project overview and instructions
```

---

## 🚀 How to Run

Make sure you have Python 3 installed. No external packages are needed.

```bash
# Run the main program
python3 main.py

# (Optional) Run the test cases
python3 test_expense_tracker.py
```
