"""
Test Suite for FinMatrics — Multi-Currency Expense Tracker & Budget Management System
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University

Covers:
- Core Test Cases 1-5 from Milestone Report
- Currency Conversion & INR Normalization
- CSV Persistence (Saving and Loading)
- Search and Filtering Logic
"""

import os
import unittest
import tempfile
from pathlib import Path

from main import (
    load_transactions,
    save_transactions,
    get_next_id,
    validate_date,
    validate_month,
    calculate_monthly_summary,
    convert_to_inr,
    convert_currency,
    EXCHANGE_RATES
)


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Standard test transactions matching project requirements."""
        self.sample_transactions = [
            {"id": 1, "date": "2026-10-01", "type": "income", "category": "Salary", "amount": 25000.00, "currency": "INR", "amount_inr": 25000.00, "description": "Salary"},
            {"id": 2, "date": "2026-10-02", "type": "expense", "category": "Transport", "amount": 120.00, "currency": "INR", "amount_inr": 120.00, "description": "Metro"},
            {"id": 3, "date": "2026-10-04", "type": "expense", "category": "Education", "amount": 800.00, "currency": "INR", "amount_inr": 800.00, "description": "Books"},
            {"id": 4, "date": "2026-10-05", "type": "expense", "category": "Food", "amount": 450.00, "currency": "INR", "amount_inr": 450.00, "description": "Groceries"}
        ]

    # -------------------------------------------------------------------------
    # CORE TEST CASES
    # -------------------------------------------------------------------------
    def test_case_1_add_expense(self):
        """Test Case 1: Add an expense and check sequential ID generation."""
        initial_count = len(self.sample_transactions)
        next_id = get_next_id(self.sample_transactions)
        self.assertEqual(next_id, 5)

        new_record = {
            "id": next_id,
            "date": "2026-10-06",
            "type": "expense",
            "category": "Food",
            "amount": 450.00,
            "currency": "INR",
            "amount_inr": 450.00,
            "description": "Lunch"
        }
        self.sample_transactions.append(new_record)
        self.assertEqual(len(self.sample_transactions), initial_count + 1)
        self.assertEqual(self.sample_transactions[-1]["category"], "Food")
        self.assertEqual(self.sample_transactions[-1]["amount"], 450.00)

    def test_case_2_monthly_summary_calculation(self):
        """Test Case 2: Monthly Summary -> Income 25000, Expense 1370, Balance 23630."""
        summary = calculate_monthly_summary(self.sample_transactions, "2026-10")
        self.assertEqual(summary["month"], "2026-10")
        self.assertEqual(summary["count"], 4)
        self.assertEqual(summary["total_income"], 25000.00)
        self.assertEqual(summary["total_expenses"], 1370.00)
        self.assertEqual(summary["balance"], 23630.00)
        self.assertEqual(summary["balance"], summary["total_income"] - summary["total_expenses"])

    def test_case_3_highest_spending_category(self):
        """Test Case 3: Food 450, Transport 120, Education 800 -> Education is highest."""
        summary = calculate_monthly_summary(self.sample_transactions, "2026-10")
        categories = summary["categories"]
        self.assertEqual(categories["Food"], 450.00)
        self.assertEqual(categories["Transport"], 120.00)
        self.assertEqual(categories["Education"], 800.00)

        highest_cat, highest_amt = summary["highest_category"]
        self.assertEqual(highest_cat, "Education")
        self.assertEqual(highest_amt, 800.00)

    def test_case_4_budget_calculation(self):
        """Test Case 4: Budget 5000.00 -> Remaining budget 3630.00 within budget."""
        summary = calculate_monthly_summary(self.sample_transactions, "2026-10")
        budget = 5000.00
        remaining = budget - summary["total_expenses"]
        self.assertEqual(remaining, 3630.00)
        self.assertGreater(remaining, 0)

    def test_case_5_input_validation(self):
        """Test Case 5: Validation of dates and months using standard datetime."""
        self.assertTrue(validate_date("2026-10-05"))
        self.assertTrue(validate_date("2024-02-29"))  # Leap year
        self.assertFalse(validate_date("2026-02-29")) # Non-leap year
        self.assertFalse(validate_date("2026-13-45")) # Invalid month/day
        self.assertFalse(validate_date("invalid-date"))
        self.assertTrue(validate_month("2026-10"))
        self.assertFalse(validate_month("2026-15"))

    # -------------------------------------------------------------------------
    # CURRENCY CONVERSION TESTS
    # -------------------------------------------------------------------------
    def test_currency_conversion(self):
        """Verifies currency conversion to INR and between currencies."""
        # 10 USD -> 10 * 83.33 = 833.30 INR
        inr_val = convert_to_inr(10.0, "USD")
        self.assertEqual(inr_val, 833.30)

        # 100 EUR -> INR
        eur_inr = convert_to_inr(100.0, "EUR")
        self.assertEqual(eur_inr, 9091.00)

        # Same currency identity
        self.assertEqual(convert_currency(500.0, "INR", "INR"), 500.0)

        # Unknown currency defaults safely
        self.assertEqual(convert_currency(100.0, "UNKNOWN", "INR"), 100.0)

    # -------------------------------------------------------------------------
    # CSV PERSISTENCE TESTS
    # -------------------------------------------------------------------------
    def test_csv_save_and_load(self):
        """Verifies that transactions save to CSV and load back accurately."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as tmp:
            tmp_path = tmp.name

        try:
            success = save_transactions(self.sample_transactions, filename=tmp_path)
            self.assertTrue(success)

            loaded = load_transactions(filename=tmp_path)
            self.assertEqual(len(loaded), len(self.sample_transactions))
            self.assertEqual(loaded[0]["category"], "Salary")
            self.assertEqual(loaded[0]["amount"], 25000.00)
            self.assertEqual(loaded[3]["category"], "Food")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # -------------------------------------------------------------------------
    # SEARCH / FILTER TESTS
    # -------------------------------------------------------------------------
    def test_search_and_filter_logic(self):
        """Verifies filtering transactions by category and date prefix."""
        food_items = [t for t in self.sample_transactions if "food" in t["category"].lower()]
        self.assertEqual(len(food_items), 1)
        self.assertEqual(food_items[0]["category"], "Food")

        october_items = [t for t in self.sample_transactions if t["date"].startswith("2026-10")]
        self.assertEqual(len(october_items), 4)

        expenses_only = [t for t in self.sample_transactions if t["type"] == "expense"]
        self.assertEqual(len(expenses_only), 3)


if __name__ == "__main__":
    unittest.main()
