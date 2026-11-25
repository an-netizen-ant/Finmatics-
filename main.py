"""
=============================================================================
Project: FinMatrics — Multi-Currency Expense Tracker & Budget Management System
Course:  Computational Thinking and Programming (2026CSAE100)
College: Bennett University, School of Computer Science Engineering and Tech

Team Members & Collaborative Responsibilities:
1. Samriddhi Jain (S26CSEU1985) - Input validation & Menu navigation
2. Pranjaldeep Kaur (S26CSEU1934) - File handling & CSV storage engine
3. Ashu Kumar (S26CSEU1963)      - Monthly summary & Category calculations
4. Ansh Vardhan (S26CSEU1919)    - Search / Filter & Budget alerts
5. Anant Gupta (S26CSEU1940)     - Report export, Currency conversion & Integration
=============================================================================
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
CSV_FILE = "transactions.csv"
FIELDNAMES = ["id", "date", "type", "category", "amount", "currency", "description"]

# Exchange rates relative to INR (1 Unit of Foreign Currency = X INR)
EXCHANGE_RATES: Dict[str, float] = {
    "INR": 1.0,
    "USD": 83.33,
    "EUR": 90.91,
    "GBP": 105.26,
    "AED": 22.73,
    "CAD": 61.35
}

CURRENCY_SYMBOLS: Dict[str, str] = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "AED": "AED",
    "CAD": "C$"
}


# =============================================================================
# MODULE 1: CURRENCY CONVERSION (Pranjaldeep & Anant)
# =============================================================================

def convert_to_inr(amount: float, currency: str) -> float:
    """Converts an amount from a given currency into base INR."""
    curr = currency.upper().strip()
    rate = EXCHANGE_RATES.get(curr, 1.0)
    return round(amount * rate, 2)


def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """Converts an amount from one currency to another using base INR rates."""
    from_curr = from_curr.upper().strip()
    to_curr = to_curr.upper().strip()

    if from_curr not in EXCHANGE_RATES or to_curr not in EXCHANGE_RATES:
        return round(amount, 2)

    # Convert to INR first, then to target currency
    amount_in_inr = amount * EXCHANGE_RATES[from_curr]
    target_amount = amount_in_inr / EXCHANGE_RATES[to_curr]
    return round(target_amount, 2)


def get_currency_symbol(curr_code: str) -> str:
    """Returns the recognized currency symbol."""
    return CURRENCY_SYMBOLS.get(curr_code.upper().strip(), curr_code.upper().strip())


# =============================================================================
# MODULE 2: CSV STORAGE ENGINE (Pranjaldeep Kaur)
# =============================================================================

def load_transactions(filename: str = CSV_FILE) -> List[Dict[str, Any]]:
    """Loads all transactions from the CSV file into a list of dictionaries."""
    file_path = Path(filename)
    if not file_path.exists():
        return []

    transactions: List[Dict[str, Any]] = []
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Clean up keys and values
                    clean_row = {k.strip().lower(): v.strip() for k, v in row.items() if k}
                    
                    trans_id = int(clean_row.get("id", 0))
                    date_str = clean_row.get("date", "")
                    trans_type = clean_row.get("type", "").lower()
                    category = clean_row.get("category", "")
                    amount = float(clean_row.get("amount", 0.0))
                    currency = clean_row.get("currency", "INR").upper()
                    description = clean_row.get("description", "")

                    if trans_type not in ["income", "expense"] or amount <= 0:
                        continue

                    amount_inr = convert_to_inr(amount, currency)

                    transactions.append({
                        "id": trans_id,
                        "date": date_str,
                        "type": trans_type,
                        "category": category,
                        "amount": amount,
                        "currency": currency,
                        "amount_inr": amount_inr,
                        "description": description
                    })
                except (ValueError, KeyError):
                    continue
    except (IOError, OSError):
        return []

    return transactions


def save_transactions(transactions: List[Dict[str, Any]], filename: str = CSV_FILE) -> bool:
    """Saves the list of transactions back to the CSV file."""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    "id": t["id"],
                    "date": t["date"],
                    "type": t["type"],
                    "category": t["category"],
                    "amount": t["amount"],
                    "currency": t.get("currency", "INR"),
                    "description": t.get("description", "")
                })
        return True
    except (IOError, OSError):
        return False


def get_next_id(transactions: List[Dict[str, Any]]) -> int:
    """Returns the next sequential unique ID for a new transaction."""
    if not transactions:
        return 1
    return max(t["id"] for t in transactions) + 1


# =============================================================================
# MODULE 3: INPUT VALIDATION (Samriddhi Jain)
# =============================================================================

def validate_date(date_str: str) -> bool:
    """Checks if a string is a valid date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_month(month_str: str) -> bool:
    """Checks if a string is a valid month in YYYY-MM format."""
    try:
        datetime.strptime(month_str.strip(), "%Y-%m")
        return True
    except ValueError:
        return False


def get_validated_date(prompt: str = "Date (YYYY-MM-DD, press Enter for today): ") -> str:
    """Prompts the user until a valid calendar date is provided."""
    while True:
        val = input(prompt).strip()
        if val == "":
            return datetime.now().strftime("%Y-%m-%d")
        if validate_date(val):
            return val
        print("Invalid date format. Please enter in YYYY-MM-DD format (e.g., 2026-10-15).")


def get_validated_type(prompt: str = "Type (income/expense): ") -> str:
    """Prompts the user until either 'income' or 'expense' is entered."""
    while True:
        val = input(prompt).strip().lower()
        if val in ["income", "expense"]:
            return val
        print("Invalid type! Please enter either 'income' or 'expense'.")


def get_validated_category(prompt: str = "Category (e.g. Food, Travel, Salary): ") -> str:
    """Prompts the user for a category name (cannot be empty)."""
    while True:
        cat = input(prompt).strip()
        if cat:
            return cat.title()
        print("Category cannot be blank. Please enter a valid name.")


def get_validated_amount(prompt: str = "Amount: ") -> float:
    """Prompts until a positive numeric amount is entered."""
    while True:
        val = input(prompt).strip()
        try:
            amt = float(val)
            if amt > 0:
                return round(amt, 2)
            print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input! Please enter a valid number (e.g., 450.50).")


def get_validated_currency(prompt: str = "Currency (INR, USD, EUR, GBP, AED, CAD - Enter for INR): ") -> str:
    """Prompts for currency code; defaults to INR if left empty."""
    while True:
        curr = input(prompt).strip().upper()
        if curr == "":
            return "INR"
        if curr in EXCHANGE_RATES:
            return curr
        print(f"Unsupported currency! Available options: {', '.join(EXCHANGE_RATES.keys())}")


def get_validated_month(prompt: str = "Month (YYYY-MM, press Enter for current): ") -> str:
    """Prompts for a month; defaults to current year-month if empty."""
    while True:
        val = input(prompt).strip()
        if val == "":
            return datetime.now().strftime("%Y-%m")
        if validate_month(val):
            return val
        print("Invalid month! Please enter in YYYY-MM format (e.g., 2026-10).")


# =============================================================================
# MODULE 4: CORE LEDGER OPERATIONS (Samriddhi & Pranjaldeep)
# =============================================================================

def add_transaction(transactions: List[Dict[str, Any]]) -> None:
    """Adds a new income or expense transaction."""
    print("\n--- Add New Transaction ---")
    date_str = get_validated_date()
    trans_type = get_validated_type()
    category = get_validated_category()
    amount = get_validated_amount()
    currency = get_validated_currency()
    description = input("Description (optional): ").strip()

    amount_inr = convert_to_inr(amount, currency)
    trans_id = get_next_id(transactions)

    new_tx = {
        "id": trans_id,
        "date": date_str,
        "type": trans_type,
        "category": category,
        "amount": amount,
        "currency": currency,
        "amount_inr": amount_inr,
        "description": description
    }

    transactions.append(new_tx)
    if save_transactions(transactions):
        print(f"\n[Success] Transaction #{trans_id} recorded successfully!")
        if currency != "INR":
            print(f"Note: Converted to ₹{amount_inr:.2f} INR for ledger records.")
    else:
        print("\n[Error] Failed to save transaction to file.")


def view_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Displays all transactions in a clean tabular format."""
    print("\n--- All Recorded Transactions ---")
    if not transactions:
        print("No transactions found in the ledger.")
        return

    print("=" * 82)
    print(f"{'ID':<4} | {'Date':<10} | {'Type':<7} | {'Category':<15} | {'Original Amount':<16} | {'Amount (INR)':>12}")
    print("=" * 82)

    for t in sorted(transactions, key=lambda x: x["date"]):
        sym = get_currency_symbol(t.get("currency", "INR"))
        orig_amt = f"{sym}{t['amount']:.2f} {t.get('currency', 'INR')}"
        print(f"{t['id']:<4} | {t['date']:<10} | {t['type'].capitalize():<7} | "
              f"{t['category']:<15} | {orig_amt:<16} | ₹{t['amount_inr']:>10.2f}")

    print("=" * 82)
    print(f"Total Transactions: {len(transactions)}")


def delete_transaction(transactions: List[Dict[str, Any]]) -> None:
    """Deletes a transaction by its unique ID."""
    print("\n--- Delete Transaction ---")
    if not transactions:
        print("No transactions available to delete.")
        return

    val = input("Enter Transaction ID to delete: ").strip()
    try:
        trans_id = int(val)
    except ValueError:
        print("Invalid ID. Please enter an integer number.")
        return

    target = None
    for t in transactions:
        if t["id"] == trans_id:
            target = t
            break

    if not target:
        print(f"Transaction with ID #{trans_id} not found.")
        return

    print(f"\nFound: #{target['id']} | {target['date']} | {target['type']} | {target['category']} | ₹{target['amount_inr']:.2f}")
    confirm = input("Are you sure you want to delete this transaction? (y/n): ").strip().lower()
    if confirm in ["y", "yes"]:
        transactions.remove(target)
        if save_transactions(transactions):
            print(f"[Success] Transaction #{trans_id} deleted successfully.")
        else:
            print("[Error] Failed to update file.")
    else:
        print("Deletion cancelled.")


# =============================================================================
# MODULE 5: SEARCH & FILTER (Ansh Vardhan)
# =============================================================================

def search_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Filters transactions by Category or Date."""
    print("\n--- Search & Filter Transactions ---")
    print("1. Search by Category")
    print("2. Search by Date")
    print("3. Filter by Type (Income / Expense)")
    choice = input("Enter option (1-3): ").strip()

    results = []
    if choice == "1":
        query = input("Enter Category to search: ").strip().lower()
        results = [t for t in transactions if query in t["category"].lower()]
    elif choice == "2":
        query = input("Enter Date (YYYY-MM-DD or YYYY-MM): ").strip()
        results = [t for t in transactions if t["date"].startswith(query)]
    elif choice == "3":
        query = get_validated_type()
        results = [t for t in transactions if t["type"] == query]
    else:
        print("Invalid search choice.")
        return

    if not results:
        print("\nNo matching transactions found.")
        return

    print(f"\n--- Found {len(results)} Matching Transactions ---")
    print("=" * 82)
    print(f"{'ID':<4} | {'Date':<10} | {'Type':<7} | {'Category':<15} | {'Amount (INR)':>12} | {'Description'}")
    print("=" * 82)
    for t in results:
        desc = t.get("description", "")
        print(f"{t['id']:<4} | {t['date']:<10} | {t['type'].capitalize():<7} | "
              f"{t['category']:<15} | ₹{t['amount_inr']:>10.2f} | {desc}")
    print("=" * 82)


# =============================================================================
# MODULE 6: MONTHLY SUMMARY & CALCULATIONS (Ashu Kumar)
# =============================================================================

def calculate_monthly_summary(transactions: List[Dict[str, Any]], target_month: str) -> Dict[str, Any]:
    """Calculates total income, total expenses, balance, and category totals for a month."""
    month_records = [t for t in transactions if t["date"].startswith(target_month)]

    total_income = 0.0
    total_expenses = 0.0
    category_totals: Dict[str, float] = {}

    for t in month_records:
        amt = t["amount_inr"]
        if t["type"] == "income":
            total_income += amt
        elif t["type"] == "expense":
            total_expenses += amt
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0.0) + amt

    balance = total_income - total_expenses

    highest_category = ("None", 0.0)
    if category_totals:
        highest_cat = max(category_totals, key=category_totals.get)
        highest_category = (highest_cat, category_totals[highest_cat])

    return {
        "month": target_month,
        "count": len(month_records),
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(balance, 2),
        "categories": category_totals,
        "highest_category": highest_category,
        "records": month_records
    }


def display_monthly_summary(transactions: List[Dict[str, Any]]) -> None:
    """Displays a formatted monthly overview."""
    print("\n--- Monthly Financial Summary ---")
    month_str = get_validated_month()
    summary = calculate_monthly_summary(transactions, month_str)

    print(f"\n==================================================")
    print(f"         FINANCIAL SUMMARY FOR {month_str}")
    print(f"==================================================")
    print(f"Total Transactions: {summary['count']}")
    print(f"Total Income:       ₹{summary['total_income']:>10.2f}")
    print(f"Total Expenses:     ₹{summary['total_expenses']:>10.2f}")
    print(f"Net Balance:        ₹{summary['balance']:>10.2f}")
    print("-" * 50)

    if summary["categories"]:
        print("Category-wise Expense Breakdown:")
        for cat, amt in sorted(summary["categories"].items(), key=lambda x: x[1], reverse=True):
            pct = (amt / summary["total_expenses"] * 100) if summary["total_expenses"] > 0 else 0
            print(f"  • {cat:<18}: ₹{amt:>9.2f}  ({pct:5.1f}%)")
        print("-" * 50)
        highest_cat, highest_amt = summary["highest_category"]
        print(f"Top Spending Category: {highest_cat} (₹{highest_amt:.2f})")
    else:
        print("No expenses recorded for this month.")
    print("=" * 50)


# =============================================================================
# MODULE 7: BUDGET ALERT CHECKER (Ansh Vardhan)
# =============================================================================

def check_budget(transactions: List[Dict[str, Any]]) -> None:
    """Compares monthly expenses against a user-defined budget limit."""
    print("\n--- Monthly Budget Check & Alerts ---")
    month_str = get_validated_month()
    summary = calculate_monthly_summary(transactions, month_str)

    budget = get_validated_amount("Enter monthly expense budget limit (in INR): ")
    total_spent = summary["total_expenses"]
    remaining = budget - total_spent

    print(f"\n==================================================")
    print(f"           BUDGET REPORT FOR {month_str}")
    print(f"==================================================")
    print(f"Set Budget:        ₹{budget:>10.2f}")
    print(f"Actual Expenses:   ₹{total_spent:>10.2f}")
    print(f"Remaining Budget:  ₹{remaining:>10.2f}")
    print("-" * 50)

    if remaining > 0:
        pct_used = (total_spent / budget) * 100
        print(f"[STATUS: SAFE] You are within budget ({pct_used:.1f}% used).")
    elif remaining == 0:
        print("[STATUS: WARNING] You have reached your exact budget limit!")
    else:
        overspent = abs(remaining)
        print(f"[STATUS: EXCEEDED] You have overspent your budget by ₹{overspent:.2f}!")
    print("=" * 50)


# =============================================================================
# MODULE 8: CURRENCY CONVERTER & EXPORT (Anant Gupta)
# =============================================================================

def interactive_currency_converter() -> None:
    """Utility to convert between foreign currencies and INR."""
    print("\n--- Currency Quick Converter ---")
    print(f"Available Currencies: {', '.join(EXCHANGE_RATES.keys())}")
    from_curr = get_validated_currency("From Currency: ")
    to_curr = get_validated_currency("To Currency: ")
    amount = get_validated_amount(f"Enter amount in {from_curr}: ")

    converted = convert_currency(amount, from_curr, to_curr)
    from_sym = get_currency_symbol(from_curr)
    to_sym = get_currency_symbol(to_curr)

    print(f"\nResult: {from_sym}{amount:.2f} {from_curr} = {to_sym}{converted:.2f} {to_curr}")


def export_monthly_report(transactions: List[Dict[str, Any]]) -> None:
    """Exports a monthly financial summary to a clean text file."""
    print("\n--- Export Monthly Report ---")
    month_str = get_validated_month()
    summary = calculate_monthly_summary(transactions, month_str)

    filename = f"monthly_report_{month_str}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 65 + "\n")
            f.write(f"           MONTHLY FINANCIAL REPORT: {month_str}\n")
            f.write(f"           Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 65 + "\n\n")

            f.write("1. SUMMARY OVERVIEW\n")
            f.write("-" * 35 + "\n")
            f.write(f"Total Transactions: {summary['count']}\n")
            f.write(f"Total Income:       ₹{summary['total_income']:.2f}\n")
            f.write(f"Total Expenses:     ₹{summary['total_expenses']:.2f}\n")
            f.write(f"Net Savings:        ₹{summary['balance']:.2f}\n\n")

            f.write("2. EXPENSE BREAKDOWN BY CATEGORY\n")
            f.write("-" * 35 + "\n")
            if summary["categories"]:
                for cat, amt in summary["categories"].items():
                    pct = (amt / summary["total_expenses"] * 100) if summary["total_expenses"] > 0 else 0
                    f.write(f"  • {cat:<18}: ₹{amt:>9.2f} ({pct:5.1f}%)\n")
                highest_cat, highest_amt = summary["highest_category"]
                f.write(f"\nTop Spending Category: {highest_cat} (₹{highest_amt:.2f})\n\n")
            else:
                f.write("  No expenses recorded for this month.\n\n")

            f.write("3. DETAILED TRANSACTION LOG\n")
            f.write("-" * 65 + "\n")
            f.write(f"{'ID':<4} | {'Date':<10} | {'Type':<7} | {'Category':<15} | {'Amount (INR)':>12}\n")
            f.write("-" * 65 + "\n")
            for t in summary["records"]:
                f.write(f"{t['id']:<4} | {t['date']:<10} | {t['type'].capitalize():<7} | "
                        f"{t['category']:<15} | ₹{t['amount_inr']:>10.2f}\n")
            f.write("-" * 65 + "\n")
            f.write("End of Report\n")

        print(f"\n[Success] Report exported successfully to '{filename}'!")
    except (IOError, OSError) as e:
        print(f"\n[Error] Could not export report: {e}")


# =============================================================================
# MODULE 9: USER INTERFACE & MENU LOOP
# =============================================================================

def display_menu() -> None:
    """Displays the main menu options."""
    print("\n" + "=" * 55)
    print("      FINMATRICS — EXPENSE TRACKER & BUDGET SYSTEM")
    print("      Computational Thinking and Programming (2026CSAE100)")
    print("=" * 55)
    print("  1. Add Transaction (Income / Expense)")
    print("  2. View All Transactions")
    print("  3. Search / Filter Transactions (by Category, Date, Type)")
    print("  4. Monthly Summary & Category Breakdown")
    print("  5. Check Monthly Budget & Alerts")
    print("  6. Delete Transaction")
    print("  7. Currency Converter")
    print("  8. Export Monthly Report to Text File")
    print("  0. Exit")
    print("-" * 55)


def main() -> None:
    """Main program execution loop."""
    transactions = load_transactions(CSV_FILE)

    while True:
        display_menu()
        choice = input("Enter choice (0-8): ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            search_transactions(transactions)
        elif choice == "4":
            display_monthly_summary(transactions)
        elif choice == "5":
            check_budget(transactions)
        elif choice == "6":
            delete_transaction(transactions)
        elif choice == "7":
            interactive_currency_converter()
        elif choice == "8":
            export_monthly_report(transactions)
        elif choice == "0":
            print("\nThank you for using FinMatrics! Goodbye.")
            break
        else:
            print("Invalid option! Please enter a number between 0 and 8.")


if __name__ == "__main__":
    main()
