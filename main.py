"""
=============================================================================
Project: FinMatrics — Intelligent Multi-Currency Expense Tracker & Financial Advisory System
Course:  Computational Thinking and Programming (2026CSAE100)
College: Bennett University, School of Computer Science Engineering and Tech

Team Members & Collaborative Responsibilities:
1. Samriddhi Jain (S26CSEU1985) - Input validation, menu dispatch, 50/30/20 scoring
2. Pranjaldeep Kaur (S26CSEU1934) - CSV storage architecture, currency conversion
3. Ashu Kumar (S26CSEU1963)      - Monthly engine, surplus wealth advisory & SIP
4. Ansh Vardhan (S26CSEU1919)    - Anomaly detection, subscriptions, testing suite
5. Anant Gupta (S26CSEU1940)     - Report export, integration, code optimization
=============================================================================
"""

import csv
import json
import difflib
import math
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any, Set

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
CSV_FILE = "transactions.csv"
FIELDNAMES = ["id", "date", "type", "category", "amount", "currency", "description", "is_recurring"]

# Base currency is INR (₹). Rates are pegged relative to 1 INR for offline crash-proof conversion.
EXCHANGE_RATES: Dict[str, float] = {
    "INR": 1.0,         # Base currency
    "USD": 0.012,       # 1 INR = 0.012 USD  (1 USD ≈ 83.33 INR)
    "EUR": 0.011,       # 1 INR = 0.011 EUR  (1 EUR ≈ 90.91 INR)
    "GBP": 0.0095,      # 1 INR = 0.0095 GBP (1 GBP ≈ 105.26 INR)
    "JPY": 1.85,        # 1 INR = 1.85 JPY   (1 JPY ≈ 0.54 INR)
    "AED": 0.044,       # 1 INR = 0.044 AED  (1 AED ≈ 22.73 INR)
    "CAD": 0.0163       # 1 INR = 0.0163 CAD (1 CAD ≈ 61.35 INR)
}

CURRENCY_SYMBOLS: Dict[str, str] = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AED": "د.إ",
    "CAD": "C$"
}

# Standard 50/30/20 category classifications
NEEDS_CATEGORIES = {"food", "groceries", "rent", "transport", "utilities", "bills", "education", "healthcare", "medical"}
WANTS_CATEGORIES = {"dining out", "entertainment", "shopping", "streaming", "electronics", "travel", "hobbies", "snacks"}
SAVINGS_CATEGORIES = {"investment", "savings", "sip", "emergency fund", "mutual funds", "fixed deposit"}


# =============================================================================
# MODULE 1: MULTI-CURRENCY CONVERSION ENGINE (Service A)
# =============================================================================

def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """
    Converts amount between any supported currencies using the base INR exchange rate matrix.
    Safe from crashing: Defaults to original amount if currency code is unrecognized.
    Formula: amount_in_base = amount / rate[from_curr]
             amount_in_target = amount_in_base * rate[to_curr]
    """
    from_curr = from_curr.upper()
    to_curr = to_curr.upper()

    if from_curr not in EXCHANGE_RATES or to_curr not in EXCHANGE_RATES:
        return round(amount, 2)

    if from_curr == to_curr:
        return round(amount, 2)

    # Convert to base (INR) first, then to target currency
    amount_in_inr = amount / EXCHANGE_RATES[from_curr]
    converted = amount_in_inr * EXCHANGE_RATES[to_curr]
    return round(converted, 2)


def get_currency_symbol(curr_code: str) -> str:
    """Returns the recognized currency symbol or the currency code itself."""
    return CURRENCY_SYMBOLS.get(curr_code.upper(), curr_code.upper())


# =============================================================================
# MODULE 2: CSV STORAGE & PERSISTENCE ENGINE (Crash-Proof)
# =============================================================================

def load_transactions(filename: str = CSV_FILE) -> List[Dict[str, Any]]:
    """
    Loads all transactions from the CSV file into a list of dictionaries.
    Resilient: Automatically recovers missing columns, handles older schema versions,
    skips malformed rows without crashing, and normalizes amounts to base INR.
    """
    file_path = Path(filename)
    if not file_path.exists():
        return []

    transactions: List[Dict[str, Any]] = []
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            # First peek at the header line
            reader = csv.reader(file)
            first_row = next(reader, None)
            if first_row is None:
                return []

            first_row_lower = [col.strip().lower() for col in first_row if col]
            has_id_header = "id" in first_row_lower

            file.seek(0)
            if has_id_header:
                # Standard DictReader with case-insensitive key normalization
                dict_reader = csv.DictReader(file)
                for raw_row in dict_reader:
                    # Normalize keys to lowercase
                    row = {k.strip().lower(): v for k, v in raw_row.items() if k}
                    try:
                        trans_id = int(row.get("id", "").strip())
                        date_str = row.get("date", "").strip()
                        trans_type = row.get("type", "").strip().lower()
                        category = row.get("category", "").strip()
                        amount = float(row.get("amount", "").strip())
                        currency = row.get("currency", "INR").strip().upper()
                        if currency not in EXCHANGE_RATES:
                            currency = "INR"

                        description = row.get("description", "").strip()
                        is_rec = row.get("is_recurring", "no").strip().lower()
                        is_recurring = is_rec in ("yes", "true", "1", "y")

                        if trans_type not in ("income", "expense") or amount <= 0:
                            continue

                        amount_inr = convert_currency(amount, currency, "INR")
                        transactions.append({
                            "id": trans_id,
                            "date": date_str,
                            "type": trans_type,
                            "category": category,
                            "amount": amount,
                            "currency": currency,
                            "amount_inr": amount_inr,
                            "description": description,
                            "is_recurring": is_recurring
                        })
                    except (ValueError, KeyError, AttributeError):
                        continue
            else:
                # Positional fallback (Header is missing, corrupted, or headerless data)
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) < 5:
                        continue
                    try:
                        trans_id = int(row[0].strip())
                        date_str = row[1].strip()
                        trans_type = row[2].strip().lower()
                        category = row[3].strip()
                        amount = float(row[4].strip())
                        currency = row[5].strip().upper() if len(row) > 5 else "INR"
                        if currency not in EXCHANGE_RATES:
                            currency = "INR"
                        description = row[6].strip() if len(row) > 6 else ""
                        is_rec = row[7].strip().lower() if len(row) > 7 else "no"
                        is_recurring = is_rec in ("yes", "true", "1", "y")

                        if trans_type not in ("income", "expense") or amount <= 0:
                            continue

                        amount_inr = convert_currency(amount, currency, "INR")
                        transactions.append({
                            "id": trans_id,
                            "date": date_str,
                            "type": trans_type,
                            "category": category,
                            "amount": amount,
                            "currency": currency,
                            "amount_inr": amount_inr,
                            "description": description,
                            "is_recurring": is_recurring
                        })
                    except (ValueError, IndexError):
                        continue
    except (IOError, OSError) as e:
        print(f"File access notice for '{filename}': {e}")
        return []

    return transactions


def save_transactions(transactions: List[Dict[str, Any]], filename: str = CSV_FILE) -> bool:
    """
    Saves the list of transactions to CSV. Creates parent directory if missing.
    """
    file_path = Path(filename)
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    "id": t["id"],
                    "date": t["date"],
                    "type": t["type"],
                    "category": t["category"],
                    "amount": f"{t['amount']:.2f}",
                    "currency": t.get("currency", "INR"),
                    "description": t.get("description", ""),
                    "is_recurring": "yes" if t.get("is_recurring", False) else "no"
                })
        return True
    except (IOError, OSError) as e:
        print(f"Error saving to '{filename}': {e}")
        return False


def get_next_id(transactions: List[Dict[str, Any]]) -> int:
    """Returns the next unique sequential ID."""
    if not transactions:
        return 1
    return max(t["id"] for t in transactions) + 1


# =============================================================================
# MODULE 3: DEFENSIVE INPUT VALIDATION & SMART TYPO-ASSISTANT
# =============================================================================

# Natural language keyword dictionary for menu options
MENU_KEYWORDS: Dict[str, str] = {
    # Option 1: Add Transaction
    "1": "1", "add": "1", "ad": "1", "new": "1", "insert": "1", "record": "1", "create": "1",
    # Option 2: View Transactions
    "2": "2", "view": "2", "vw": "2", "show": "2", "see": "2", "display": "2", "list": "2", "all": "2",
    # Option 3: Monthly Summary
    "3": "3", "summary": "3", "summry": "3", "sumary": "3", "month": "3", "monthly": "3", "totals": "3",
    # Option 4: Budget Check
    "4": "4", "budget": "4", "budgt": "4", "bdgt": "4", "limit": "4", "check": "4",
    # Option 5: Delete Transaction
    "5": "5", "delete": "5", "del": "5", "remove": "5", "rm": "5", "erase": "5", "cancel": "5",
    # Option 6: 50/30/20 Financial Health Scorecard
    "6": "6", "scorecard": "6", "score": "6", "health": "6", "503020": "6", "ratio": "6", "grade": "6",
    # Option 7: Surplus Wealth Allocation & SIP
    "7": "7", "wealth": "7", "invest": "7", "investment": "7", "advisory": "7", "sip": "7", "surplus": "7", "compound": "7",
    # Option 8: Expense Leak & Anomaly Detection
    "8": "8", "leak": "8", "leaks": "8", "anomaly": "8", "anomalies": "8", "spike": "8", "habit": "8", "pattern": "8",
    # Option 9: Recurring Subscriptions
    "9": "9", "subscription": "9", "subscriptions": "9", "subs": "9", "recurring": "9", "bills": "9", "squeeze": "9",
    # Option 10: Multi-Currency Quick Converter
    "10": "10", "convert": "10", "converter": "10", "currency": "10", "forex": "10", "exchange": "10", "fx": "10",
    # Option 11: Comprehensive Audit Report
    "11": "11", "export": "11", "report": "11", "audit": "11", "file": "11", "txt": "11", "save": "11",
    # Option 12: Financial Runway & Burn Rate Calculator
    "12": "12", "runway": "12", "burn": "12", "velocity": "12", "runwy": "12",
    # Option 13: Month-over-Month Trend & Variance
    "13": "13", "trend": "13", "trends": "13", "mom": "13", "variance": "13",
    # Option 14: JSON Structured Backup
    "14": "14", "backup": "14", "json": "14", "bakup": "14",
    # Option 0: Exit
    "0": "0", "exit": "0", "quit": "0", "q": "0", "bye": "0", "close": "0", "stop": "0"
}

TYPE_ALIASES: Dict[str, str] = {
    "income": "income", "incom": "income", "incoem": "income", "inc": "income", "salary": "income", "deposit": "income", "earning": "income", "earn": "income",
    "expense": "expense", "expnse": "expense", "expanse": "expense", "exp": "expense", "spent": "expense", "spending": "expense", "cost": "expense"
}

CURRENCY_ALIASES: Dict[str, str] = {
    "inr": "INR", "inrr": "INR", "rupee": "INR", "rupees": "INR", "rs": "INR", "₹": "INR",
    "usd": "USD", "usdd": "USD", "dollar": "USD", "dollars": "USD", "buck": "USD", "bucks": "USD", "$": "USD",
    "eur": "EUR", "eruo": "EUR", "uero": "EUR", "euro": "EUR", "euros": "EUR", "€": "EUR",
    "gbp": "GBP", "pound": "GBP", "pounds": "GBP", "quid": "GBP", "£": "GBP",
    "jpy": "JPY", "yen": "JPY", "¥": "JPY",
    "aed": "AED", "dirham": "AED", "dirhams": "AED",
    "cad": "CAD", "cad dollar": "CAD", "canadian": "CAD"
}


def resolve_smart_menu_choice(raw_input: str) -> Optional[str]:
    """
    Intelligently maps numeric options, keywords, and typos to valid menu choices.
    Uses difflib to resolve spelling mistakes without crashing.
    """
    clean = raw_input.strip().lower()
    if not clean:
        return None

    # Exact keyword or number match
    if clean in MENU_KEYWORDS:
        mapped = MENU_KEYWORDS[clean]
        if clean != mapped:
            print(f"[Smart Assistant] Interpreting '{raw_input}' as option {mapped}...")
        return mapped

    # Fuzzy match close typo against recognized keywords
    candidates = list(MENU_KEYWORDS.keys())
    matches = difflib.get_close_matches(clean, candidates, n=1, cutoff=0.6)
    if matches:
        best_match = matches[0]
        mapped = MENU_KEYWORDS[best_match]
        print(f"[Smart Assistant] Typo detected: Interpreting '{raw_input}' as '{best_match}' (Option {mapped}).")
        return mapped

    return None


def normalize_date_input(val: str) -> str:
    """
    Normalizes minor formatting typos like '2026/10/05' or '2026-1-5' into '2026-01-05'.
    """
    clean = val.strip().replace("/", "-").replace(".", "-").replace(" ", "")
    parts = clean.split("-")
    if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        year = parts[0]
        month = parts[1].zfill(2)
        day = parts[2].zfill(2)
        return f"{year}-{month}-{day}"
    return clean


def normalize_month_input(val: str) -> str:
    """
    Normalizes minor formatting typos like '2026/10' or '2026-1' into '2026-01'.
    """
    clean = val.strip().replace("/", "-").replace(".", "-").replace(" ", "")
    parts = clean.split("-")
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        year = parts[0]
        month = parts[1].zfill(2)
        return f"{year}-{month}"
    return clean


def validate_date(date_str: str) -> bool:
    """Validates real calendar dates in YYYY-MM-DD format (rejects 2026-02-29, etc.)."""
    try:
        norm = normalize_date_input(date_str)
        datetime.strptime(norm, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_month(month_str: str) -> bool:
    """Validates real month in YYYY-MM format."""
    try:
        norm = normalize_month_input(month_str)
        datetime.strptime(norm, "%Y-%m")
        return True
    except ValueError:
        return False


def get_validated_date(prompt: str = "Date (YYYY-MM-DD, blank for today): ") -> str:
    """Prompts until a valid date is entered; auto-normalizes slashes/dots and defaults to today."""
    while True:
        val = input(prompt).strip()
        if val == "":
            return datetime.now().strftime("%Y-%m-%d")
        norm = normalize_date_input(val)
        if validate_date(norm):
            if norm != val:
                print(f"[Smart Assistant] Auto-formatted date to '{norm}'.")
            return norm
        print("Invalid date. Please enter a valid calendar date in YYYY-MM-DD format (e.g. 2026-10-05).")


def get_validated_type(prompt: str = "Type (income/expense): ") -> str:
    """Prompts until user enters 'income' or 'expense', with auto-correction for typos."""
    while True:
        val = input(prompt).strip().lower()
        if val in TYPE_ALIASES:
            resolved = TYPE_ALIASES[val]
            if val != resolved:
                print(f"[Smart Assistant] Typo corrected: '{val}' -> '{resolved}'.")
            return resolved

        # Fuzzy match
        matches = difflib.get_close_matches(val, ["income", "expense"], n=1, cutoff=0.6)
        if matches:
            resolved = matches[0]
            print(f"[Smart Assistant] Typo corrected: Interpreting '{val}' as '{resolved}'.")
            return resolved

        print("Invalid type. Please enter either 'income' or 'expense'.")


def get_validated_category(prompt: str = "Category: ", existing_categories: Optional[Set[str]] = None) -> str:
    """Prompts for a category, offering smart suggestions for typos against existing categories."""
    while True:
        cat = input(prompt).strip()
        if not cat:
            print("Category cannot be blank. Please enter a valid category name.")
            continue

        cat_title = cat.title()
        if existing_categories:
            matches = difflib.get_close_matches(cat_title, list(existing_categories), n=1, cutoff=0.75)
            if matches and matches[0] != cat_title:
                best = matches[0]
                print(f"[Smart Assistant] Typo detected: Did you mean existing category '{best}'? Auto-selected '{best}'.")
                return best

        return cat_title


def get_validated_amount(prompt: str = "Amount: ") -> float:
    """Prompts until a positive numeric float is provided."""
    while True:
        val = input(prompt).strip().replace(",", "")  # Strip formatting commas
        try:
            amt = float(val)
            if amt <= 0:
                print("Amount must be a positive number greater than 0.")
                continue
            return round(amt, 2)
        except ValueError:
            print("Invalid number. Please enter a valid numeric amount (e.g. 450.00).")


def get_validated_currency(prompt: str = f"Currency ({', '.join(EXCHANGE_RATES.keys())}, blank for INR): ") -> str:
    """Prompts for currency code; understands aliases (dollar, euro, etc.) and fixes typos."""
    while True:
        curr = input(prompt).strip().lower()
        if curr == "":
            return "INR"

        if curr in CURRENCY_ALIASES:
            resolved = CURRENCY_ALIASES[curr]
            if curr.upper() != resolved:
                print(f"[Smart Assistant] Resolved currency '{curr}' -> '{resolved}'.")
            return resolved

        # Fuzzy match against supported currencies and aliases
        all_candidates = list(EXCHANGE_RATES.keys()) + list(CURRENCY_ALIASES.keys())
        matches = difflib.get_close_matches(curr, all_candidates, n=1, cutoff=0.6)
        if matches:
            match_key = matches[0]
            resolved = CURRENCY_ALIASES.get(match_key, match_key.upper())
            print(f"[Smart Assistant] Typo corrected: Interpreting '{curr}' as '{resolved}'.")
            return resolved

        print(f"Unsupported currency '{curr}'. Supported options: {', '.join(EXCHANGE_RATES.keys())}")


def get_validated_month(prompt: str = "Month (YYYY-MM, blank for current): ") -> str:
    """Prompts for month (YYYY-MM); defaults to current year-month and normalizes formatting."""
    while True:
        val = input(prompt).strip()
        if val == "":
            return datetime.now().strftime("%Y-%m")
        norm = normalize_month_input(val)
        if validate_month(norm):
            if norm != val:
                print(f"[Smart Assistant] Auto-formatted month to '{norm}'.")
            return norm
        print("Invalid month format. Please enter YYYY-MM (e.g. 2026-10).")


def get_validated_confirmation(prompt: str = "Confirm? (y/n): ", default: bool = False) -> bool:
    """
    Asks user for a yes/no confirmation with typo-tolerant affirmative/negative understanding.
    """
    AFFIRMATIVE = {"y", "yes", "ye", "yeah", "yep", "sure", "ok", "true", "1", "ys", "yea"}
    NEGATIVE = {"n", "no", "nope", "nah", "false", "0", "nn"}

    while True:
        ans = input(prompt).strip().lower()
        if ans == "":
            return default
        if ans in AFFIRMATIVE:
            return True
        if ans in NEGATIVE:
            return False

        # Fuzzy match close typos
        if difflib.get_close_matches(ans, ["yes", "yeah"], n=1, cutoff=0.6):
            print(f"[Smart Assistant] Typo corrected: Interpreting '{ans}' as 'yes'.")
            return True
        if difflib.get_close_matches(ans, ["no", "nope"], n=1, cutoff=0.6):
            print(f"[Smart Assistant] Typo corrected: Interpreting '{ans}' as 'no'.")
            return False

        print("Please answer with 'y' (yes) or 'n' (no).")


# =============================================================================
# MODULE 4: TRANSACTION MANAGEMENT (Add, View, Delete)
# =============================================================================

def add_transaction(transactions: List[Dict[str, Any]]) -> None:
    """Interactively captures a new transaction with multi-currency and recurring tags."""
    print("\n--- Add Transaction ---")
    date_val = get_validated_date("Date (YYYY-MM-DD, blank for today): ")
    type_val = get_validated_type("Type (income/expense): ")
    existing_cats = set(t["category"] for t in transactions if "category" in t)
    category_val = get_validated_category("Category: ", existing_cats)
    amount_val = get_validated_amount("Amount: ")
    curr_val = get_validated_currency()
    desc_val = input("Description (optional): ").strip()
    is_recurring = get_validated_confirmation("Is this a recurring monthly bill/subscription? (y/n, blank for n): ", default=False)

    new_id = get_next_id(transactions)
    amount_inr = convert_currency(amount_val, curr_val, "INR")

    new_record = {
        "id": new_id,
        "date": date_val,
        "type": type_val,
        "category": category_val,
        "amount": amount_val,
        "currency": curr_val,
        "amount_inr": amount_inr,
        "description": desc_val,
        "is_recurring": is_recurring
    }

    transactions.append(new_record)
    if save_transactions(transactions):
        sym = get_currency_symbol(curr_val)
        print(f"\nTransaction #{new_id} saved successfully: {sym}{amount_val:.2f} ({curr_val}).")
        if curr_val != "INR":
            print(f"Normalized base value: ₹{amount_inr:.2f} INR")
        print(f"CSV storage updated: {CSV_FILE}")
    else:
        print("\nFailed to save transaction to CSV file.")


def view_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Renders all transactions in a clean, multi-currency formatted table."""
    print("\n--- View Transactions ---")
    if not transactions:
        print("No transactions found in records.")
        return

    # User may choose viewing currency
    view_curr = input(f"Select display currency ({', '.join(EXCHANGE_RATES.keys())}, blank for native): ").strip().upper()
    convert_display = view_curr in EXCHANGE_RATES
    sym = get_currency_symbol(view_curr) if convert_display else "₹"

    sorted_list = sorted(transactions, key=lambda x: (x["date"], x["id"]))

    header = f"{'ID':<4} | {'Date':<10} | {'Type':<7} | {'Category':<15} | {'Amount':>12} | {'Recurring':<9} | {'Description'}"
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)

    total_inc_inr = 0.0
    total_exp_inr = 0.0

    for t in sorted_list:
        t_type = t["type"].capitalize()
        t_rec = "Yes" if t.get("is_recurring", False) else "No"
        desc = t.get("description", "") or "-"

        if convert_display:
            disp_amt = convert_currency(t["amount_inr"], "INR", view_curr)
            amt_str = f"{sym}{disp_amt:>10.2f}"
        else:
            t_sym = get_currency_symbol(t.get("currency", "INR"))
            amt_str = f"{t_sym}{t['amount']:>9.2f}"

        if t["type"] == "income":
            total_inc_inr += t["amount_inr"]
        else:
            total_exp_inr += t["amount_inr"]

        print(f"{t['id']:<4} | {t['date']:<10} | {t_type:<7} | {t['category']:<15} | {amt_str} | {t_rec:<9} | {desc}")

    print(sep)
    net_inr = total_inc_inr - total_exp_inr
    if convert_display and view_curr != "INR":
        disp_inc = convert_currency(total_inc_inr, "INR", view_curr)
        disp_exp = convert_currency(total_exp_inr, "INR", view_curr)
        disp_net = convert_currency(net_inr, "INR", view_curr)
        print(f"Total in {view_curr} ({sym}): Income: {disp_inc:.2f} | Expenses: {disp_exp:.2f} | Net Balance: {disp_net:.2f}")
    else:
        print(f"Total Base (₹ INR): Income: ₹{total_inc_inr:.2f} | Expenses: ₹{total_exp_inr:.2f} | Net Balance: ₹{net_inr:.2f}")
    print(sep)


def delete_transaction(transactions: List[Dict[str, Any]]) -> None:
    """Interactively locates a record by ID, asks confirmation, and removes it."""
    print("\n--- Delete Transaction ---")
    if not transactions:
        print("No transactions available to delete.")
        return

    while True:
        id_str = input("Enter Transaction ID to delete (or 'c' to cancel): ").strip()
        if id_str.lower() == "c":
            print("Deletion cancelled.")
            return
        try:
            target_id = int(id_str)
            break
        except ValueError:
            print("Please enter a valid numeric ID.")

    found_idx = None
    target_rec = None
    for idx, t in enumerate(transactions):
        if t["id"] == target_id:
            found_idx = idx
            target_rec = t
            break

    if target_rec is None:
        print(f"Transaction #{target_id} not found.")
        return

    sym = get_currency_symbol(target_rec.get("currency", "INR"))
    print(f"\nTarget: ID #{target_rec['id']} | Date: {target_rec['date']} | {target_rec['category']} | {sym}{target_rec['amount']:.2f}")
    confirm = get_validated_confirmation("Are you sure you want to permanently delete this transaction? (y/n): ", default=False)
    if confirm:
        del transactions[found_idx]
        if save_transactions(transactions):
            print(f"Transaction #{target_id} successfully deleted.")
            print(f"CSV storage updated: {CSV_FILE}")
        else:
            print("Error writing changes to CSV file.")
    else:
        print("Deletion cancelled.")


# =============================================================================
# MODULE 5: COMPUTATIONAL MONTHLY SUMMARY & BUDGET ENGINE
# =============================================================================

def calculate_monthly_summary(transactions: List[Dict[str, Any]], target_month: str) -> Dict[str, Any]:
    """
    Computes all core financial aggregates for target month (YYYY-MM) in base INR.
    Returns income, expenses, balance, count, and category breakdown.
    """
    month_records = [t for t in transactions if t["date"].startswith(target_month)]

    total_income = 0.0
    total_expenses = 0.0
    category_expenses: Dict[str, float] = {}

    for t in month_records:
        amt = t["amount_inr"]
        if t["type"] == "income":
            total_income += amt
        elif t["type"] == "expense":
            total_expenses += amt
            cat = t["category"]
            category_expenses[cat] = category_expenses.get(cat, 0.0) + amt

    balance = total_income - total_expenses
    highest_category: Optional[Tuple[str, float]] = None

    if category_expenses:
        sorted_cats = sorted(category_expenses.items(), key=lambda item: item[1], reverse=True)
        highest_category = sorted_cats[0]

    return {
        "month": target_month,
        "records": month_records,
        "count": len(month_records),
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(balance, 2),
        "categories": category_expenses,
        "highest_category": highest_category
    }



def render_ascii_bar_chart(category_totals: Dict[str, float], total_spent: float, max_bars: int = 20) -> str:
    """Renders a clean ASCII horizontal bar chart representing category expense distribution."""
    if total_spent <= 0 or not category_totals:
        return ""
    lines = ["\nVisual Category Distribution (ASCII Bar Chart):", "-" * 55]
    for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total_spent) * 100
        bars = int(round((pct / 100) * max_bars))
        bar_str = "█" * bars + "░" * (max_bars - bars)
        lines.append(f"  {cat:<14} | {bar_str} | {pct:5.1f}% (₹{amt:>8.2f})")
    lines.append("-" * 55)
    return "\n".join(lines)

def display_monthly_summary(transactions: List[Dict[str, Any]]) -> None:
    """Interactive monthly summary with optional currency conversion display."""
    print("\n--- Monthly Summary ---")
    month_str = get_validated_month("Month (YYYY-MM, blank for current): ")
    summary = calculate_monthly_summary(transactions, month_str)

    curr_choice = input(f"Currency for summary ({', '.join(EXCHANGE_RATES.keys())}, blank for INR): ").strip().upper()
    display_curr = curr_choice if curr_choice in EXCHANGE_RATES else "INR"
    sym = get_currency_symbol(display_curr)

    inc = convert_currency(summary["total_income"], "INR", display_curr)
    exp = convert_currency(summary["total_expenses"], "INR", display_curr)
    bal = convert_currency(summary["balance"], "INR", display_curr)

    print(f"\n--- Monthly Summary ({display_curr}) ---")
    print(f"Month:          {summary['month']}")
    print(f"Total income:   {sym}{inc:.2f}")
    print(f"Total expenses: {sym}{exp:.2f}")
    print(f"Balance:        {sym}{bal:.2f}")
    print(f"Transactions:   {summary['count']}")

    if summary["categories"]:
        print("\nExpense categories:")
        for cat in sorted(summary["categories"].keys()):
            cat_amt = convert_currency(summary["categories"][cat], "INR", display_curr)
            pct = (cat_amt / exp * 100) if exp > 0 else 0
            print(f"  - {cat:<15}: {sym}{cat_amt:>8.2f} ({pct:5.1f}%)")

        highest_cat, highest_amt_inr = summary["highest_category"]
        highest_disp = convert_currency(highest_amt_inr, "INR", display_curr)
        print(f"\nHighest spending category: {highest_cat} ({sym}{highest_disp:.2f})")
    else:
        print("\nNo expense records found for this month.")


def check_budget(transactions: List[Dict[str, Any]]) -> None:
    """Evaluates spending against an entered monthly budget with multi-tier alerts."""
    print("\n--- Budget Check ---")
    month_str = get_validated_month("Month (YYYY-MM, blank for current): ")
    budget = get_validated_amount("Enter monthly budget (in INR): ")

    summary = calculate_monthly_summary(transactions, month_str)
    expenses = summary["total_expenses"]
    remaining = budget - expenses
    spent_pct = (expenses / budget * 100) if budget > 0 else 0.0

    print("\n--- Budget Analysis Results ---")
    print(f"Target Month:       {month_str}")
    print(f"Allocated Budget:   ₹{budget:.2f}")
    print(f"Total Expenses:     ₹{expenses:.2f}")
    print(f"Remaining Budget:   ₹{remaining:.2f}")
    print(f"Budget Utilized:    {spent_pct:.2f}%")

    if remaining > 0:
        print(f"Status: Within budget. You have ₹{remaining:.2f} remaining.")
        if spent_pct > 85.0:
            print("Caution Alert: You have utilized over 85% of your allocated budget!")
    elif remaining == 0:
        print("Status: Exactly on budget. Zero surplus remaining.")
    else:
        print(f"Status: BUDGET EXCEEDED! You have overspent by ₹{abs(remaining):.2f}.")


# =============================================================================
# MODULE 6: 50 / 30 / 20 FINANCIAL HEALTH SCORECARD (Service C)
# =============================================================================

def analyze_50_30_20_health(transactions: List[Dict[str, Any]], month_str: str) -> Dict[str, Any]:
    """
    Computes 50/30/20 personal finance rule breakdown:
      - Needs: Target <= 50%
      - Wants: Target <= 30%
      - Savings: Target >= 20%
    Computes an algorithmic Financial Health Score (0 to 100) and actionable advice.
    """
    summary = calculate_monthly_summary(transactions, month_str)
    total_income = summary["total_income"]
    total_expenses = summary["total_expenses"]

    needs_total = 0.0
    wants_total = 0.0
    savings_total = 0.0

    for t in summary["records"]:
        if t["type"] == "expense":
            cat_clean = t["category"].strip().lower()
            amt = t["amount_inr"]
            if cat_clean in SAVINGS_CATEGORIES:
                savings_total += amt
            elif cat_clean in WANTS_CATEGORIES:
                wants_total += amt
            else:
                # Default unknown categories to Needs
                needs_total += amt

    # Net monthly savings = (Income - Expenses) + recorded savings transactions
    actual_savings = max(0.0, total_income - total_expenses) + savings_total
    denominator = total_income if total_income > 0 else (total_expenses + actual_savings)

    if denominator == 0:
        return {
            "month": month_str,
            "income": 0.0,
            "needs_total": 0.0,
            "needs_pct": 0.0,
            "wants_total": 0.0,
            "wants_pct": 0.0,
            "savings_total": 0.0,
            "savings_pct": 0.0,
            "score": 100.0,
            "grade": "N/A (No Transaction Data Recorded)",
            "recommendations": ["No transactions recorded for this month to evaluate."]
        }

    needs_pct = (needs_total / denominator * 100) if denominator > 0 else 0.0
    wants_pct = (wants_total / denominator * 100) if denominator > 0 else 0.0
    savings_pct = (actual_savings / denominator * 100) if denominator > 0 else 0.0

    # Algorithmic Scoring (100 baseline)
    score = 100.0
    # Penalty for Needs over 50%
    if needs_pct > 50.0:
        score -= min(40.0, (needs_pct - 50.0) * 1.5)
    # Penalty for Wants over 30%
    if wants_pct > 30.0:
        score -= min(40.0, (wants_pct - 30.0) * 2.0)
    # Penalty for Savings below 20%
    if savings_pct < 20.0:
        score -= min(40.0, (20.0 - savings_pct) * 2.0)

    score = max(0.0, min(100.0, round(score, 1)))

    if score >= 85:
        grade = "A (Excellent Financial Health)"
    elif score >= 70:
        grade = "B (Good / Stable)"
    elif score >= 50:
        grade = "C (Needs Attention)"
    else:
        grade = "D (High Financial Stress)"

    recommendations = []
    if needs_pct > 50:
        recommendations.append(f"Needs consume {needs_pct:.1f}% of income (ideal <= 50%). Consider reviewing recurring utility or rent costs.")
    if wants_pct > 30:
        recommendations.append(f"Wants consume {wants_pct:.1f}% of income (ideal <= 30%). Reducing dining out/shopping by ₹{(wants_total * 0.25):.2f} would restore balance.")
    if savings_pct < 20:
        recommendations.append(f"Savings rate is {savings_pct:.1f}% (ideal >= 20%). Automate transfer of at least ₹{(denominator * 0.2 - actual_savings):.2f} at start of month.")
    if not recommendations:
        recommendations.append("Outstanding financial discipline! You adhere strictly to the 50/30/20 wealth formula.")

    return {
        "month": month_str,
        "income": total_income,
        "needs_total": needs_total,
        "needs_pct": round(needs_pct, 1),
        "wants_total": wants_total,
        "wants_pct": round(wants_pct, 1),
        "savings_total": actual_savings,
        "savings_pct": round(savings_pct, 1),
        "score": score,
        "grade": grade,
        "recommendations": recommendations
    }


def display_50_30_20_scorecard(transactions: List[Dict[str, Any]]) -> None:
    """UI for 50/30/20 Financial Health Scorecard."""
    print("\n--- 50/30/20 Financial Health Scorecard ---")
    month_str = get_validated_month("Month (YYYY-MM, blank for current): ")
    result = analyze_50_30_20_health(transactions, month_str)

    print(f"\n==================================================")
    print(f"  50/30/20 FINANCIAL HEALTH SCORECARD ({month_str})")
    print(f"==================================================")
    print(f"Total Reference Income: ₹{result['income']:.2f}")
    print("-" * 50)
    print(f"1. Needs   (Target <= 50%): ₹{result['needs_total']:>9.2f}  [{result['needs_pct']:>5.1f}%]")
    print(f"2. Wants   (Target <= 30%): ₹{result['wants_total']:>9.2f}  [{result['wants_pct']:>5.1f}%]")
    print(f"3. Savings (Target >= 20%): ₹{result['savings_total']:>9.2f}  [{result['savings_pct']:>5.1f}%]")
    print("-" * 50)
    print(f"FINANCIAL HEALTH SCORE: {result['score']} / 100")
    print(f"RATING GRADE:           {result['grade']}")
    print("-" * 50)
    print("Actionable Recommendations:")
    for idx, rec in enumerate(result["recommendations"], start=1):
        print(f"  {idx}. {rec}")
    print("=" * 50)


# =============================================================================
# MODULE 7: SURPLUS WEALTH ALLOCATION & SIP ADVISORY (Service B)
# =============================================================================

def calculate_sip_future_value(monthly_investment: float, annual_return_rate: float, years: int) -> float:
    """
    Calculates future compound value of monthly SIP:
    Formula: FV = P * [ ((1 + r)^n - 1) / r ] * (1 + r)
    where r = annual_return_rate / 12 / 100, n = years * 12
    """
    if monthly_investment <= 0 or years <= 0:
        return 0.0
    r = (annual_return_rate / 100) / 12
    n = years * 12
    if r == 0:
        return monthly_investment * n
    fv = monthly_investment * (((math.pow(1 + r, n) - 1) / r) * (1 + r))
    return round(fv, 2)


def generate_wealth_advisory(surplus_inr: float, risk_profile: str) -> Dict[str, Any]:
    """
    Generates tailored asset allocation for surplus capital based on risk profile:
      1. Conservative (Student / Capital Preservation)
      2. Moderate (Balanced Index Investing)
      3. Growth (Aggressive Compounding)
    """
    risk_profile = risk_profile.lower()

    if "conservative" in risk_profile:
        alloc = {
            "Emergency High-Yield Buffer (FD / Liquid)": 0.50,
            "Safe Recurring Deposit / Debt Fund": 0.30,
            "Skill Upskilling & Education Fund": 0.20
        }
        exp_return = 7.0
    elif "growth" in risk_profile or "aggressive" in risk_profile:
        alloc = {
            "Diversified Equity / Nifty 50 Index SIP": 0.65,
            "Tech Skills & Professional Certifications": 0.20,
            "Emergency Liquidity Cushion": 0.15
        }
        exp_return = 13.0
    else:  # Moderate (Default)
        alloc = {
            "Nifty 50 / Broad Market Index Fund SIP": 0.50,
            "High-Yield Emergency Buffer": 0.30,
            "Skill Mastery & Books / Courses": 0.20
        }
        exp_return = 11.5

    breakdown = {}
    for asset, weight in alloc.items():
        breakdown[asset] = round(surplus_inr * weight, 2)

    # Calculate 1-yr, 3-yr, and 5-yr growth for the investment portion
    invest_amt = breakdown.get("Nifty 50 / Broad Market Index Fund SIP",
                               breakdown.get("Diversified Equity / Nifty 50 Index SIP",
                                             breakdown.get("Safe Recurring Deposit / Debt Fund", 0.0)))

    projections = {
        "1_year": calculate_sip_future_value(invest_amt, exp_return, 1),
        "3_years": calculate_sip_future_value(invest_amt, exp_return, 3),
        "5_years": calculate_sip_future_value(invest_amt, exp_return, 5)
    }

    return {
        "surplus": surplus_inr,
        "profile": risk_profile.capitalize(),
        "allocations": breakdown,
        "invest_amt": invest_amt,
        "exp_return": exp_return,
        "projections": projections
    }


def surplus_wealth_advisory_service(transactions: List[Dict[str, Any]]) -> None:
    """Interactive wealth allocation advisor for unspent budget or savings."""
    print("\n--- Surplus Wealth Allocation & Investment Advisor ---")
    month_str = get_validated_month("Month to evaluate (YYYY-MM, blank for current): ")
    summary = calculate_monthly_summary(transactions, month_str)

    surplus = summary["balance"]
    print(f"\nNet Savings for {month_str}: ₹{surplus:.2f} (Income: ₹{summary['total_income']:.2f} - Expenses: ₹{summary['total_expenses']:.2f})")

    if surplus <= 0:
        print("Notice: No surplus capital available for this month (Expenses >= Income).")
        print("Advisory Tip: Focus on reviewing your highest spending category to eliminate non-essential expenses.")
        return

    print("\nChoose your Risk Horizon & Goal:")
    print("  1. Conservative (Student / Capital Protection - Liquid & Safe)")
    print("  2. Moderate     (Balanced Wealth Creation - Index SIP & Skills)")
    print("  3. Growth       (Aggressive Compounding - High Equity Index)")
    choice = input("Select profile (1-3, default 2): ").strip()

    if choice == "1":
        profile = "conservative"
    elif choice == "3":
        profile = "growth"
    else:
        profile = "moderate"

    advisory = generate_wealth_advisory(surplus, profile)

    print(f"\n==================================================")
    print(f"  SMART ASSET ALLOCATION FOR ₹{surplus:.2f} SURPLUS")
    print(f"  Selected Profile: {advisory['profile']}")
    print(f"==================================================")
    for asset, amt in advisory["allocations"].items():
        pct = (amt / surplus * 100) if surplus > 0 else 0
        print(f"  • {asset:<42}: ₹{amt:>9.2f} ({pct:4.1f}%)")

    print(f"\n--- Compound Growth Simulator (Monthly SIP @ {advisory['exp_return']}% p.a.) ---")
    monthly_sip = advisory["invest_amt"]
    print(f"If you consistently invest this ₹{monthly_sip:.2f}/month:")
    print(f"  • In 1 Year:  ₹{advisory['projections']['1_year']:>10.2f} (Invested: ₹{(monthly_sip * 12):.2f})")
    print(f"  • In 3 Years: ₹{advisory['projections']['3_years']:>10.2f} (Invested: ₹{(monthly_sip * 36):.2f})")
    print(f"  • In 5 Years: ₹{advisory['projections']['5_years']:>10.2f} (Invested: ₹{(monthly_sip * 60):.2f})")
    print("=" * 50)


# =============================================================================
# MODULE 8: EXPENSE "LEAK" & ANOMALY DETECTION (Service D)
# =============================================================================

def detect_expense_leaks_and_anomalies(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computational pattern detection:
      1. Micro-spending habit leak: Identifies frequent small transactions (< ₹250) in
         casual categories (Snacks, Food, Entertainment) and calculates annual drain.
      2. Statistical spending anomalies: Flags transactions that are > 2x the category average.
    """
    expense_records = [t for t in transactions if t["type"] == "expense"]
    if not expense_records:
        return {"leaks": [], "anomalies": []}

    # 1. Micro-spending leak analysis
    micro_expenses: Dict[str, List[float]] = {}
    for t in expense_records:
        if t["amount_inr"] <= 250.0:
            cat = t["category"]
            if cat not in micro_expenses:
                micro_expenses[cat] = []
            micro_expenses[cat].append(t["amount_inr"])

    leaks = []
    for cat, amounts in micro_expenses.items():
        if len(amounts) >= 3:
            total_spent = sum(amounts)
            annual_impact = total_spent * 12  # Projected annual drain
            leaks.append({
                "category": cat,
                "count": len(amounts),
                "total_spent": round(total_spent, 2),
                "annual_impact": round(annual_impact, 2)
            })

    # 2. Category averages & Spikes
    cat_totals: Dict[str, List[float]] = {}
    for t in expense_records:
        cat = t["category"]
        if cat not in cat_totals:
            cat_totals[cat] = []
        cat_totals[cat].append(t["amount_inr"])

    anomalies = []
    for t in expense_records:
        cat = t["category"]
        history = cat_totals[cat]
        if len(history) >= 2:
            # Baseline average of other transactions in this category
            other_sum = sum(history) - t["amount_inr"]
            other_count = len(history) - 1
            baseline_avg = (other_sum / other_count) if other_count > 0 else (sum(history) / len(history))
            if baseline_avg > 0 and t["amount_inr"] >= 2.0 * baseline_avg and t["amount_inr"] >= 500.0:
                anomalies.append({
                    "id": t["id"],
                    "date": t["date"],
                    "category": cat,
                    "amount": t["amount_inr"],
                    "average": round(baseline_avg, 2),
                    "multiplier": round(t["amount_inr"] / baseline_avg, 1),
                    "desc": t.get("description", "-")
                })

    return {"leaks": leaks, "anomalies": anomalies}


def display_expense_leaks_and_anomalies(transactions: List[Dict[str, Any]]) -> None:
    """UI for Expense Leak and Anomaly Detection."""
    print("\n--- Expense Leak & Anomaly Detection (Pattern Identification) ---")
    results = detect_expense_leaks_and_anomalies(transactions)

    print("\n1. MICRO-SPENDING HABIT LEAKS (The 'Latte Factor' / UPI Drain):")
    print("-" * 60)
    if results["leaks"]:
        for leak in results["leaks"]:
            print(f"  • Category: {leak['category']}")
            print(f"    {leak['count']} small transactions totaling ₹{leak['total_spent']:.2f}")
            print(f"    PROJECTED ANNUAL DRAIN: ₹{leak['annual_impact']:.2f}/year if continued!")
    else:
        print("  No repetitive micro-spending leaks detected. Excellent discipline!")

    print("\n2. UNUSUAL SPENDING SPIKES & ANOMALIES (> 2x Category Average):")
    print("-" * 60)
    if results["anomalies"]:
        for anom in results["anomalies"]:
            print(f"  • [ID #{anom['id']}] {anom['date']} | {anom['category']}: ₹{anom['amount']:.2f}")
            print(f"    Category Average: ₹{anom['average']:.2f} (Spike is {anom['multiplier']}x normal)")
            print(f"    Description: {anom['desc']}")
    else:
        print("  No abnormal expenditure spikes detected across categories.")
    print("-" * 60)


# =============================================================================
# MODULE 9: RECURRING SUBSCRIPTION & BILL SQUEEZE DETECTOR (Service F)
# =============================================================================

def analyze_recurring_subscriptions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Identifies recurring subscriptions/bills by either explicit tags or repetitive
    monthly occurrences, computing monthly burn and annual financial commitment.
    """
    subscriptions: Dict[str, float] = {}

    for t in transactions:
        if t["type"] == "expense" and t.get("is_recurring", False):
            cat_desc = f"{t['category']} ({t.get('description', 'Subscription')})"
            # Store the latest recurring amount
            subscriptions[cat_desc] = t["amount_inr"]

    # Also detect auto-candidates (same category & identical amount occurring > 1 time)
    if not subscriptions:
        candidates: Dict[Tuple[str, float], int] = {}
        for t in transactions:
            if t["type"] == "expense":
                key = (t["category"], t["amount_inr"])
                candidates[key] = candidates.get(key, 0) + 1
        for (cat, amt), count in candidates.items():
            if count >= 2 and cat.lower() in ("utilities", "streaming", "entertainment", "bills"):
                subscriptions[f"{cat} (Auto-detected)"] = amt

    monthly_total = sum(subscriptions.values())
    annual_total = monthly_total * 12

    return {
        "subscriptions": subscriptions,
        "monthly_burn": round(monthly_total, 2),
        "annual_burn": round(annual_total, 2)
    }


def display_recurring_subscriptions(transactions: List[Dict[str, Any]]) -> None:
    """UI for Recurring Subscription & Bill Squeeze Detector."""
    print("\n--- Recurring Subscriptions & Bill Squeeze Detector ---")
    result = analyze_recurring_subscriptions(transactions)

    print("\n==================================================")
    print("  RECURRING COMMITMENT AUDIT")
    print("==================================================")
    if result["subscriptions"]:
        for name, amt in result["subscriptions"].items():
            print(f"  • {name:<35}: ₹{amt:>8.2f}/mo (₹{(amt * 12):>9.2f}/yr)")
        print("-" * 50)
        print(f"TOTAL MONTHLY RECURRING BURN: ₹{result['monthly_burn']:.2f}")
        print(f"TOTAL ANNUAL COMMITTED COST:  ₹{result['annual_burn']:.2f}")
        print("-" * 50)
        print("Squeeze Recommendation:")
        print(f"  Pausing even 1 non-essential subscription can free up ₹3,000–₹6,000")
        print(f"  annually towards your compound investment or emergency fund.")
    else:
        print("  No recurring subscriptions or bills recorded yet.")
        print("  Tip: When adding transactions, answer 'y' to recurring to track them here.")
    print("=" * 50)


# =============================================================================
# MODULE 10: MULTI-CURRENCY CONVERTER CALCULATOR
# =============================================================================

def interactive_currency_converter() -> None:
    """Instant utility allowing users to convert between any supported currencies."""
    print("\n--- Multi-Currency Quick Converter ---")
    print(f"Supported Currencies: {', '.join(EXCHANGE_RATES.keys())}")
    from_curr = get_validated_currency("From Currency (e.g. USD, EUR, INR): ")
    to_curr = get_validated_currency("To Currency (e.g. INR, USD, EUR): ")
    amount = get_validated_amount(f"Enter amount in {from_curr}: ")

    converted = convert_currency(amount, from_curr, to_curr)
    from_sym = get_currency_symbol(from_curr)
    to_sym = get_currency_symbol(to_curr)

    print(f"\nResult: {from_sym}{amount:.2f} {from_curr} = {to_sym}{converted:.2f} {to_curr}")
    print(f"Exchange Rate: 1 {from_curr} = {(convert_currency(1.0, from_curr, to_curr)):.4f} {to_curr}")


# =============================================================================
# MODULE 11: AUDIT REPORT EXPORT
# =============================================================================

def export_monthly_report(transactions: List[Dict[str, Any]]) -> None:
    """Generates an extensive audit text file incorporating analytics, scorecards & advice."""
    print("\n--- Export Comprehensive Audit Report ---")
    month_str = get_validated_month("Month (YYYY-MM, blank for current): ")
    summary = calculate_monthly_summary(transactions, month_str)
    scorecard = analyze_50_30_20_health(transactions, month_str)
    advisory = generate_wealth_advisory(max(0.0, summary["balance"]), "moderate")
    subscriptions = analyze_recurring_subscriptions(transactions)

    report_filename = f"monthly_report_{month_str}.txt"

    try:
        with open(report_filename, "w", encoding="utf-8") as rep:
            rep.write("=" * 70 + "\n")
            rep.write(f"  COMPREHENSIVE FINANCIAL AUDIT & INTELLIGENT REPORT: {month_str}\n")
            rep.write(f"  Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            rep.write("=" * 70 + "\n\n")

            rep.write("1. EXECUTIVE SUMMARY (BASE INR)\n")
            rep.write("-" * 40 + "\n")
            rep.write(f"Total Transactions: {summary['count']}\n")
            rep.write(f"Total Income:       ₹{summary['total_income']:.2f}\n")
            rep.write(f"Total Expenses:     ₹{summary['total_expenses']:.2f}\n")
            rep.write(f"Net Savings:        ₹{summary['balance']:.2f}\n\n")

            rep.write("2. CATEGORY BREAKDOWN\n")
            rep.write("-" * 40 + "\n")
            if summary["categories"]:
                for cat in sorted(summary["categories"].keys()):
                    amt = summary["categories"][cat]
                    pct = (amt / summary["total_expenses"] * 100) if summary["total_expenses"] > 0 else 0
                    rep.write(f"  - {cat:<18}: ₹{amt:>9.2f} ({pct:5.1f}%)\n")
                highest_cat, highest_amt = summary["highest_category"]
                rep.write(f"\nHighest Spending Category: {highest_cat} (₹{highest_amt:.2f})\n\n")
            else:
                rep.write("  No expense categories recorded for this month.\n\n")

            rep.write("3. 50/30/20 FINANCIAL HEALTH SCORECARD\n")
            rep.write("-" * 40 + "\n")
            rep.write(f"Financial Health Score: {scorecard['score']} / 100 [{scorecard['grade']}]\n")
            rep.write(f"Needs:   {scorecard['needs_pct']}% (Target <= 50%)\n")
            rep.write(f"Wants:   {scorecard['wants_pct']}% (Target <= 30%)\n")
            rep.write(f"Savings: {scorecard['savings_pct']}% (Target >= 20%)\n\n")

            rep.write("4. SURPLUS WEALTH ALLOCATION ADVISORY\n")
            rep.write("-" * 40 + "\n")
            rep.write(f"Evaluated Surplus: ₹{advisory['surplus']:.2f}\n")
            for asset, amt in advisory["allocations"].items():
                rep.write(f"  • {asset}: ₹{amt:.2f}\n")
            rep.write(f"SIP 5-Year Projection: ₹{advisory['projections']['5_years']:.2f}\n\n")

            rep.write("5. RECURRING SUBSCRIPTIONS & COMMITTED COSTS\n")
            rep.write("-" * 40 + "\n")
            rep.write(f"Monthly Recurring Burn: ₹{subscriptions['monthly_burn']:.2f}\n")
            rep.write(f"Annual Committed Cost:  ₹{subscriptions['annual_burn']:.2f}\n\n")

            rep.write("6. DETAILED TRANSACTION LOG\n")
            rep.write("-" * 70 + "\n")
            rep.write(f"{'ID':<4} | {'Date':<10} | {'Type':<7} | {'Category':<15} | {'Amount (INR)':>12} | {'Description'}\n")
            rep.write("-" * 70 + "\n")
            for t in summary["records"]:
                desc = t.get("description", "-") or "-"
                rep.write(f"{t['id']:<4} | {t['date']:<10} | {t['type'].capitalize():<7} | "
                          f"{t['category']:<15} | ₹{t['amount_inr']:>10.2f} | {desc}\n")
            rep.write("-" * 70 + "\n")
            rep.write("End of Audit Report\n")

        print(f"\nComprehensive report exported successfully to: {report_filename}")
    except (IOError, OSError) as e:
        print(f"Error exporting report: {e}")



# =============================================================================
# MODULE 12: FINANCIAL RUNWAY & CASHFLOW VELOCITY (Service G)
# =============================================================================

def calculate_financial_runway(transactions: List[Dict[str, Any]], liquid_savings_inr: float) -> Dict[str, Any]:
    """
    Computes daily spending velocity, average monthly burn rate, and financial survival runway.
    Formula: Runway (Months) = Liquid Reserve / Average Monthly Burn
    """
    expense_records = [t for t in transactions if t["type"] == "expense"]
    if not expense_records:
        return {
            "savings": liquid_savings_inr,
            "evaluated_months": 0,
            "monthly_burn": 0.0,
            "daily_velocity": 0.0,
            "runway_months": float("inf") if liquid_savings_inr > 0 else 0.0,
            "status": "No Expense Records",
            "safe_daily_budget": round(liquid_savings_inr / 30, 2)
        }

    months_seen: Dict[str, float] = {}
    for t in expense_records:
        m = t["date"][:7]
        months_seen[m] = months_seen.get(m, 0.0) + t["amount_inr"]

    num_months = len(months_seen)
    total_spent = sum(months_seen.values())
    avg_monthly_burn = total_spent / num_months if num_months > 0 else 0.0
    avg_daily_velocity = avg_monthly_burn / 30.0

    if avg_monthly_burn > 0:
        runway_months = round(liquid_savings_inr / avg_monthly_burn, 1)
    else:
        runway_months = float("inf")

    if runway_months >= 6.0:
        status = "FORTRESS BUFFER (6+ Months - Excellent Financial Security)"
    elif runway_months >= 3.0:
        status = "HEALTHY (3 to 6 Months - Standard Recommended Emergency Cushion)"
    elif runway_months >= 1.0:
        status = "MODERATE (1 to 3 Months - Maintain spending discipline)"
    else:
        status = "CRITICAL (< 1 Month Runway - High risk of liquidity depletion!)"

    today = datetime.now()
    days_left = max(1, 30 - today.day)
    safe_daily = round(liquid_savings_inr / days_left, 2) if days_left > 0 else 0.0

    return {
        "savings": round(liquid_savings_inr, 2),
        "evaluated_months": num_months,
        "monthly_burn": round(avg_monthly_burn, 2),
        "daily_velocity": round(avg_daily_velocity, 2),
        "runway_months": runway_months,
        "status": status,
        "safe_daily_budget": safe_daily
    }


def display_financial_runway(transactions: List[Dict[str, Any]]) -> None:
    """UI for Financial Runway and Cashflow Burn Velocity."""
    print("\n--- Financial Runway & Cashflow Burn Velocity ---")
    current_savings = get_validated_amount("Enter your current total bank/liquid savings (in INR): ")
    result = calculate_financial_runway(transactions, current_savings)

    print(f"\n==================================================")
    print("  FINANCIAL RUNWAY & CASHFLOW VELOCITY AUDIT")
    print(f"==================================================")
    print(f"Current Liquid Reserves:    ₹{result['savings']:>10.2f}")
    print(f"Months Analyzed:            {result['evaluated_months']} month(s)")
    print(f"Average Monthly Burn Rate:  ₹{result['monthly_burn']:>10.2f} / month")
    print(f"Daily Spending Velocity:    ₹{result['daily_velocity']:>10.2f} / day")
    print("-" * 50)
    print(f"ESTIMATED FINANCIAL RUNWAY: {result['runway_months']} Months")
    print(f"STATUS ASSESSMENT:          {result['status']}")
    print("-" * 50)
    print(f"Recommended Safe Daily Pace: ₹{result['safe_daily_budget']:.2f} / day for remainder of month.")
    print("=" * 50)


# =============================================================================
# MODULE 13: MONTH-OVER-MONTH (MoM) TREND ANALYSIS (Service H)
# =============================================================================

def analyze_monthly_trends(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes chronological Month-over-Month (MoM) expenditure trend, variance deltas,
    and spending trajectory across recorded months.
    """
    monthly_data: Dict[str, Dict[str, float]] = {}
    for t in transactions:
        m = t["date"][:7]
        if m not in monthly_data:
            monthly_data[m] = {"income": 0.0, "expense": 0.0}
        if t["type"] == "income":
            monthly_data[m]["income"] += t["amount_inr"]
        else:
            monthly_data[m]["expense"] += t["amount_inr"]

    sorted_months = sorted(monthly_data.keys())
    trends = []

    prev_exp = None
    for m in sorted_months:
        inc = monthly_data[m]["income"]
        exp = monthly_data[m]["expense"]
        net = inc - exp

        if prev_exp is None or prev_exp == 0:
            delta_pct = 0.0
            direction = "BASELINE"
        else:
            delta_pct = round(((exp - prev_exp) / prev_exp) * 100, 1)
            direction = f"▲ +{delta_pct}%" if delta_pct > 0 else (f"▼ {delta_pct}%" if delta_pct < 0 else "FLAT 0.0%")

        trends.append({
            "month": m,
            "income": round(inc, 2),
            "expense": round(exp, 2),
            "net": round(net, 2),
            "delta_pct": delta_pct,
            "direction": direction
        })
        prev_exp = exp

    return trends


def display_monthly_trends(transactions: List[Dict[str, Any]]) -> None:
    """UI for Month-over-Month Spending Trends."""
    print("\n--- Month-over-Month (MoM) Spending Trend & Variance ---")
    trends = analyze_monthly_trends(transactions)
    if not trends:
        print("No transactions available to analyze trends.")
        return

    print("\n=====================================================================")
    print(f"{'Month':<8} | {'Income (INR)':>12} | {'Expenses (INR)':>14} | {'Net Savings':>12} | {'MoM Variance'}")
    print("=====================================================================")
    for t in trends:
        print(f"{t['month']:<8} | ₹{t['income']:>10.2f} | ₹{t['expense']:>12.2f} | ₹{t['net']:>10.2f} | {t['direction']}")
    print("=====================================================================")


# =============================================================================
# MODULE 14: JSON STRUCTURED LEDGER BACKUP (Service I)
# =============================================================================

def export_json_backup(transactions: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """Exports entire ledger as a structured, versioned JSON backup file."""
    if not filename:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_ledger_{date_str}.json"

    backup_payload = {
        "metadata": {
            "app": "FinMatrics",
            "version": "2.0.0",
            "exported_at": datetime.now().isoformat(),
            "total_records": len(transactions),
            "base_currency": "INR"
        },
        "transactions": transactions
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backup_payload, f, indent=2)

    return filename


def interactive_json_backup(transactions: List[Dict[str, Any]]) -> None:
    """Interactive handler for JSON backup export."""
    print("\n--- JSON Structured Ledger Backup ---")
    out_file = export_json_backup(transactions)
    print(f"[Success] Full ledger ({len(transactions)} records) backed up to JSON:")
    print(f"          -> {out_file}")

# =============================================================================
# MODULE 15: USER INTERFACE & MAIN LOOP
# =============================================================================

def display_menu() -> None:
    """Renders the comprehensive CLI options menu."""
    print("\n" + "=" * 65)
    print("  FINMATRICS — INTELLIGENT FINANCIAL ADVISORY SYSTEM")
    print("  Computational Thinking and Programming (2026CSAE100)")
    print("=" * 65)
    print("--- CORE OPERATIONS ---")
    print("  1. Add Transaction (Multi-Currency & Recurring Tag)")
    print("  2. View Transactions (Tabular & Multi-Currency)")
    print("  3. Monthly Summary (Income, Expenses, Category Breakdown)")
    print("  4. Budget Check & Spending Alerts")
    print("  5. Delete Transaction")
    print("\n--- INTELLIGENT COMPUTATIONAL SERVICES ---")
    print("  6. 50/30/20 Financial Health Scorecard (Scoring Engine)")
    print("  7. Surplus Wealth Allocation & SIP Advisory (Investment Engine)")
    print("  8. Expense Leak & Anomaly Detection (Pattern Identification)")
    print("  9. Recurring Subscriptions & Bill Squeeze Detector")
    print(" 10. Multi-Currency Quick Converter")
    print("\n--- REPORTING & SYSTEM ---")
    print(" 11. Export Comprehensive Audit Report (.txt)")
    print("  0. Exit")
    print("-" * 65)


def main() -> None:
    """Main execution loop with crash-proof option handling and typo resolution."""
    transactions = load_transactions(CSV_FILE)

    while True:
        display_menu()
        raw_choice = input("Choose an option (0-14 or keyword): ").strip()
        choice = resolve_smart_menu_choice(raw_choice)

        if choice is None:
            print(f"Option '{raw_choice}' not recognized. Please choose 0 to 14 (or type a keyword like 'add', 'summary', 'exit').")
            continue

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            display_monthly_summary(transactions)
        elif choice == "4":
            check_budget(transactions)
        elif choice == "5":
            delete_transaction(transactions)
        elif choice == "6":
            display_50_30_20_scorecard(transactions)
        elif choice == "7":
            surplus_wealth_advisory_service(transactions)
        elif choice == "8":
            display_expense_leaks_and_anomalies(transactions)
        elif choice == "9":
            display_recurring_subscriptions(transactions)
        elif choice == "10":
            interactive_currency_converter()
        elif choice == "11":
            export_monthly_report(transactions)
        elif choice == "12":
            display_financial_runway(transactions)
        elif choice == "13":
            display_monthly_trends(transactions)
        elif choice == "14":
            interactive_json_backup(transactions)
        elif choice == "0":
            print("\nThank you for using Python Expense Tracker & Financial Advisor. Goodbye!")
            break


if __name__ == "__main__":
    main()
