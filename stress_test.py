"""
Automated Stress-Testing and Fuzzing Harness
Validates crash-resistance across extreme edge cases, invalid inputs,
boundary limits, and corrupted files.
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime

# Import functions from main.py
from main import (
    load_transactions,
    save_transactions,
    get_next_id,
    validate_date,
    validate_month,
    convert_currency,
    calculate_sip_future_value,
    analyze_50_30_20_health,
    generate_wealth_advisory,
    detect_expense_leaks_and_anomalies,
    analyze_recurring_subscriptions,
    calculate_monthly_summary,
    EXCHANGE_RATES,
    CURRENCY_SYMBOLS
)

class TestFuzzAndExtremeEdgeCases(unittest.TestCase):

    # 1. CURRENCY ENGINE FUZZING
    def test_currency_extreme_cases(self):
        # Unrecognized currency code
        self.assertEqual(convert_currency(100.0, "UNKNOWN", "INR"), 100.0)
        self.assertEqual(convert_currency(100.0, "INR", "NONEXISTENT"), 100.0)
        self.assertEqual(convert_currency(100.0, "", ""), 100.0)
        # Lowercase / Mixed case handling
        self.assertAlmostEqual(convert_currency(100.0, "usd", "inr"), 8333.33, places=1)
        self.assertAlmostEqual(convert_currency(100.0, "InR", "UsD"), 1.2, places=1)
        # Zero amount
        self.assertEqual(convert_currency(0.0, "USD", "INR"), 0.0)
        # Massive amount
        large_amt = 10**9
        converted = convert_currency(large_amt, "USD", "INR")
        self.assertTrue(converted > 0)

    # 2. SIP MATHEMATICS & BOUNDARIES
    def test_sip_extreme_values(self):
        # 0 years
        self.assertEqual(calculate_sip_future_value(5000, 12, 0), 0.0)
        # 0 investment
        self.assertEqual(calculate_sip_future_value(0, 12, 5), 0.0)
        # Negative parameters
        self.assertEqual(calculate_sip_future_value(-100, 12, 5), 0.0)
        self.assertEqual(calculate_sip_future_value(500, 12, -2), 0.0)
        # 0% interest rate (Linear sum: P * n)
        self.assertEqual(calculate_sip_future_value(1000, 0, 1), 12000.0)

    # 3. 50/30/20 SCORECARD CORNER CASES
    def test_scorecard_corner_cases(self):
        # Empty dataset
        res = analyze_50_30_20_health([], "2026-10")
        self.assertEqual(res["score"], 100.0)
        self.assertIn("N/A", res["grade"])

        # 100% Needs (Over limit of 50%)
        records_needs_only = [
            {"id": 1, "type": "expense", "category": "Rent", "amount_inr": 10000.0, "date": "2026-10-01"}
        ]
        res_needs = analyze_50_30_20_health(records_needs_only, "2026-10")
        self.assertTrue(res_needs["score"] < 100.0)

        # 100% Wants (Over limit of 30%)
        records_wants_only = [
            {"id": 1, "type": "expense", "category": "Shopping", "amount_inr": 10000.0, "date": "2026-10-01"}
        ]
        res_wants = analyze_50_30_20_health(records_wants_only, "2026-10")
        self.assertTrue(res_wants["score"] < 100.0)

        # 100% Savings
        records_savings_only = [
            {"id": 1, "type": "income", "category": "Salary", "amount_inr": 50000.0, "date": "2026-10-01"}
        ]
        res_savings = analyze_50_30_20_health(records_savings_only, "2026-10")
        self.assertEqual(res_savings["score"], 100.0)
        self.assertIn("A", res_savings["grade"])

    # 4. ANOMALY & PATTERN DETECTOR EDGES
    def test_anomaly_corner_cases(self):
        # Empty records
        self.assertEqual(detect_expense_leaks_and_anomalies([]), {"leaks": [], "anomalies": []})
        # Single record
        single = [{"id": 1, "type": "expense", "category": "Food", "amount_inr": 200.0, "date": "2026-10-01", "description": ""}]
        self.assertEqual(detect_expense_leaks_and_anomalies(single), {"leaks": [], "anomalies": []})
        # Income only records
        income_only = [{"id": 1, "type": "income", "category": "Salary", "amount_inr": 25000.0, "date": "2026-10-01", "description": ""}]
        self.assertEqual(detect_expense_leaks_and_anomalies(income_only), {"leaks": [], "anomalies": []})

    # 5. RECURRING SUBSCRIPTIONS CORNER CASES
    def test_subscriptions_corner_cases(self):
        # Empty transactions
        empty_res = analyze_recurring_subscriptions([])
        self.assertEqual(empty_res["monthly_burn"], 0.0)
        self.assertEqual(empty_res["annual_burn"], 0.0)

    # 6. WEALTH ADVISORY FOR DEFICIT
    def test_wealth_advisory_zero_or_deficit(self):
        # Zero surplus
        adv_zero = generate_wealth_advisory(0.0, "moderate")
        self.assertEqual(sum(adv_zero["allocations"].values()), 0.0)
        # Negative surplus (Deficit)
        adv_neg = generate_wealth_advisory(-500.0, "growth")
        self.assertTrue(adv_neg["surplus"] <= 0)

    # 7. CORRUPTED CSV LOAD & SAVE FAULT-TOLERANCE
    def test_corrupted_csv_handling(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as f:
            path = f.name
            # Corrupted contents: missing header, strings in numeric fields, incomplete commas, blank lines
            f.write("some,random,broken,header\n")
            f.write("\n")  # Empty line
            f.write("not_an_id,2026-10-01,expense,Food,not_an_amount,INR,Lunch,no\n")
            f.write("1,2026-10-01,expense,Food,-450.00,INR,Negative amount,no\n")
            f.write("2,2026-10-02,unknown_type,Food,500.00,INR,Invalid type,no\n")
            # Exactly one valid row among garbage
            f.write("3,2026-10-03,expense,Transport,150.00,INR,Valid Bus Fare,no\n")
            f.flush()

        try:
            records = load_transactions(path)
            # Must safely load the single valid record and skip all garbage without crashing
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["id"], 3)
            self.assertEqual(records[0]["amount"], 150.00)
        finally:
            if os.path.exists(path):
                os.remove(path)

    # 8. DATE & MONTH VALIDATION TRAPS
    def test_date_validation_traps(self):
        traps = [
            "", " ", "2026-10", "2026/10/05", "05-10-2026", "2026-02-30",
            "2026-04-31", "2025-02-29", "abcd-ef-gh", "2026-00-10", "2026-13-10"
        ]
        for t in traps:
            self.assertFalse(validate_date(t), f"Failed to reject invalid date: {t}")

        valid_dates = ["2026-01-01", "2024-02-29", "2026-12-31", "2026-10-05"]
        for v in valid_dates:
            self.assertTrue(validate_date(v), f"Failed to accept valid date: {v}")

    # 9. GET NEXT ID ON EDGE CASES
    def test_next_id_edges(self):
        self.assertEqual(get_next_id([]), 1)
        self.assertEqual(get_next_id([{"id": 42}]), 43)
        self.assertEqual(get_next_id([{"id": 5}, {"id": 12}, {"id": 2}]), 13)


if __name__ == "__main__":
    unittest.main()
