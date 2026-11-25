"""
Comprehensive Test Suite for Python Expense Tracker & Intelligent Financial Advisor
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University

Covers:
- Core Test Cases 1-5 from Milestone Report
- Service A: Multi-Currency conversion and crash-proof handling
- Service B: Surplus Wealth Allocation & SIP Compounding mathematical verification
- Service C: 50/30/20 Financial Health Scorecard & algorithmic penalties
- Service D: Expense Leak (micro-spending) & Statistical Anomaly detection
- Service F: Recurring Subscriptions & Annual Burn calculation
- Crash-proof tests: Backward compatibility with older CSV schemas, malformed inputs, ZeroDivisionError guards
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
    convert_currency,
    calculate_sip_future_value,
    analyze_50_30_20_health,
    generate_wealth_advisory,
    detect_expense_leaks_and_anomalies,
    analyze_recurring_subscriptions,
    calculate_financial_runway,
    analyze_monthly_trends,
    export_json_backup,
    EXCHANGE_RATES
)


class TestExpenseTrackerAndAdvisory(unittest.TestCase):

    def setUp(self):
        """Standardized test transactions matching university report specifications."""
        self.sample_transactions = [
            {"id": 1, "date": "2026-10-01", "type": "income", "category": "Salary", "amount": 25000.00, "currency": "INR", "amount_inr": 25000.00, "description": "Salary", "is_recurring": False},
            {"id": 2, "date": "2026-10-02", "type": "expense", "category": "Transport", "amount": 120.00, "currency": "INR", "amount_inr": 120.00, "description": "Metro", "is_recurring": False},
            {"id": 3, "date": "2026-10-04", "type": "expense", "category": "Education", "amount": 800.00, "currency": "INR", "amount_inr": 800.00, "description": "Books", "is_recurring": False},
            {"id": 4, "date": "2026-10-05", "type": "expense", "category": "Food", "amount": 450.00, "currency": "INR", "amount_inr": 450.00, "description": "Groceries", "is_recurring": False}
        ]

    # -------------------------------------------------------------------------
    # CORE TEST CASES (1 to 5 from original report)
    # -------------------------------------------------------------------------
    def test_case_1_add_expense(self):
        """Test Case 1: Add expense Food, 450.00 -> Saved successfully."""
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
            "description": "Lunch and snacks",
            "is_recurring": False
        }
        self.sample_transactions.append(new_record)
        self.assertEqual(len(self.sample_transactions), initial_count + 1)
        self.assertEqual(self.sample_transactions[-1]["category"], "Food")
        self.assertEqual(self.sample_transactions[-1]["amount"], 450.00)

    def test_case_2_monthly_summary_calculation(self):
        """Test Case 2: Month 2026-10 -> 25000.00; 1370.00; 23630.00."""
        summary = calculate_monthly_summary(self.sample_transactions, "2026-10")
        self.assertEqual(summary["month"], "2026-10")
        self.assertEqual(summary["count"], 4)
        self.assertEqual(summary["total_income"], 25000.00)
        self.assertEqual(summary["total_expenses"], 1370.00)
        self.assertEqual(summary["balance"], 23630.00)
        self.assertEqual(summary["balance"], summary["total_income"] - summary["total_expenses"])

    def test_case_3_highest_spending_category(self):
        """Test Case 3: Food 450; Transport 120; Education 800 -> Education is highest."""
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
        """Test Case 5: Defensive validation of dates, months, and formats."""
        self.assertTrue(validate_date("2026-10-05"))
        self.assertTrue(validate_date("2024-02-29"))  # Leap year
        self.assertFalse(validate_date("2026-02-29")) # Invalid (non-leap year)
        self.assertFalse(validate_date("2026-13-45")) # Invalid month/day
        self.assertFalse(validate_date("random-text"))
        self.assertTrue(validate_month("2026-10"))
        self.assertFalse(validate_month("2026-15"))

    # -------------------------------------------------------------------------
    # SERVICE A: MULTI-CURRENCY CONVERSION TESTS
    # -------------------------------------------------------------------------
    def test_currency_conversion_accuracy_and_crash_proof(self):
        """Verifies currency conversion mathematical accuracy and crash-resistance."""
        # 100 USD to INR: 100 / 0.012 = 8333.33 INR
        inr_val = convert_currency(100.0, "USD", "INR")
        self.assertAlmostEqual(inr_val, 8333.33, places=1)

        # 8333.33 INR back to USD: 8333.33 * 0.012 = 100.00 USD
        usd_val = convert_currency(8333.33, "INR", "USD")
        self.assertAlmostEqual(usd_val, 100.0, places=1)

        # Same currency identity
        self.assertEqual(convert_currency(500.0, "EUR", "EUR"), 500.0)

        # Crash-proof check: Unknown currency code returns original amount without crashing
        self.assertEqual(convert_currency(250.0, "XYZ", "INR"), 250.0)

    # -------------------------------------------------------------------------
    # SERVICE B: SURPLUS ALLOCATION & SIP COMPOUNDING TESTS
    # -------------------------------------------------------------------------
    def test_sip_compounding_future_value_formula(self):
        """Verifies monthly SIP compound future value calculation."""
        # Investing ₹5,000/month for 1 year at 12% p.a.
        # Monthly r = 0.01, n = 12. Formula: 5000 * (((1.01^12 - 1) / 0.01) * 1.01) ≈ 64046.64
        fv = calculate_sip_future_value(5000.0, 12.0, 1)
        self.assertAlmostEqual(fv, 64046.64, delta=1.0)

        # Boundary checks
        self.assertEqual(calculate_sip_future_value(0, 12.0, 3), 0.0)
        self.assertEqual(calculate_sip_future_value(1000, 12.0, 0), 0.0)

    def test_wealth_advisory_profiles(self):
        """Verifies that advisory correctly partitions surplus according to risk profile."""
        surplus = 10000.0
        advisory_mod = generate_wealth_advisory(surplus, "moderate")
        allocations = advisory_mod["allocations"]
        self.assertEqual(sum(allocations.values()), surplus)
        self.assertIn("1_year", advisory_mod["projections"])
        self.assertIn("5_years", advisory_mod["projections"])

    # -------------------------------------------------------------------------
    # SERVICE C: 50/30/20 FINANCIAL HEALTH SCORECARD TESTS
    # -------------------------------------------------------------------------
    def test_50_30_20_scoring_logic(self):
        """Verifies 50/30/20 scorecard breakdown and scoring bounds."""
        scorecard = analyze_50_30_20_health(self.sample_transactions, "2026-10")
        # In October 2026: Income 25000, Needs = 1370 (5.5%), Wants = 0%, Savings = 23630 (94.5%)
        self.assertGreaterEqual(scorecard["score"], 80.0)
        self.assertIn("A", scorecard["grade"])
        self.assertTrue(len(scorecard["recommendations"]) > 0)

        # Zero division guard check (empty month)
        empty_scorecard = analyze_50_30_20_health([], "1999-01")
        self.assertEqual(empty_scorecard["score"], 100.0)

    # -------------------------------------------------------------------------
    # SERVICE D: EXPENSE LEAK & ANOMALY DETECTION TESTS
    # -------------------------------------------------------------------------
    def test_expense_leak_and_anomaly_detection(self):
        """Verifies pattern detection of repetitive micro-spending and spikes."""
        transactions = [
            {"id": 1, "type": "expense", "category": "Snacks", "amount_inr": 50.0, "date": "2026-10-01", "description": "Tea"},
            {"id": 2, "type": "expense", "category": "Snacks", "amount_inr": 60.0, "date": "2026-10-02", "description": "Biscuits"},
            {"id": 3, "type": "expense", "category": "Snacks", "amount_inr": 40.0, "date": "2026-10-03", "description": "Coffee"},
            {"id": 4, "type": "expense", "category": "Shopping", "amount_inr": 600.0, "date": "2026-10-04", "description": "Shirt"},
            {"id": 5, "type": "expense", "category": "Shopping", "amount_inr": 3500.0, "date": "2026-10-05", "description": "Luxury Watch"}
        ]
        results = detect_expense_leaks_and_anomalies(transactions)

        # 3 snacks under ₹250 should be flagged as micro-spending leak
        self.assertEqual(len(results["leaks"]), 1)
        self.assertEqual(results["leaks"][0]["category"], "Snacks")
        self.assertEqual(results["leaks"][0]["annual_impact"], 150.0 * 12)

        # ₹3500 shopping spike should be flagged as anomaly
        self.assertTrue(any(a["amount"] == 3500.0 for a in results["anomalies"]))

    # -------------------------------------------------------------------------
    # SERVICE F: RECURRING SUBSCRIPTIONS DETECTION TESTS
    # -------------------------------------------------------------------------
    def test_recurring_subscriptions_detection(self):
        """Verifies recurring subscription detection and annual burn calculation."""
        transactions = [
            {"id": 1, "type": "expense", "category": "Streaming", "amount_inr": 1250.0, "is_recurring": True, "description": "Netflix"},
            {"id": 2, "type": "expense", "category": "Utilities", "amount_inr": 650.0, "is_recurring": True, "description": "Broadband"},
            {"id": 3, "type": "expense", "category": "Food", "amount_inr": 450.0, "is_recurring": False, "description": "Groceries"}
        ]
        sub_audit = analyze_recurring_subscriptions(transactions)
        self.assertEqual(sub_audit["monthly_burn"], 1900.00)
        self.assertEqual(sub_audit["annual_burn"], 1900.00 * 12)

    # -------------------------------------------------------------------------
    # CSV PERSISTENCE & BACKWARD COMPATIBILITY
    # -------------------------------------------------------------------------
    def test_csv_backward_compatibility_and_persistence(self):
        """Ensures old CSV schemas (without currency / is_recurring) load seamlessly."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as tmp:
            tmp_path = tmp.name
            # Write old-schema CSV header and rows
            tmp.write("id,date,type,category,amount,description\n")
            tmp.write("1,2026-10-01,income,Salary,25000.00,Stipend\n")
            tmp.write("2,2026-10-02,expense,Food,450.00,Lunch\n")

        try:
            loaded = load_transactions(tmp_path)
            self.assertEqual(len(loaded), 2)
            # Defaulted values for missing columns
            self.assertEqual(loaded[0]["currency"], "INR")
            self.assertEqual(loaded[0]["is_recurring"], False)
            self.assertEqual(loaded[0]["amount_inr"], 25000.00)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # -------------------------------------------------------------------------
    # SMART ASSISTANT: TYPO RESOLUTION & INPUT NORMALIZATION TESTS
    # -------------------------------------------------------------------------
    def test_smart_typo_resolution(self):
        """Verifies difflib-powered typo assistance across menus, dates, and aliases."""
        from main import resolve_smart_menu_choice, normalize_date_input, TYPE_ALIASES, CURRENCY_ALIASES

        # Menu typo matching
        self.assertEqual(resolve_smart_menu_choice("sumary"), "3")     # Typo: sumary -> summary
        self.assertEqual(resolve_smart_menu_choice("bdgt"), "4")       # Typo: bdgt -> budget
        self.assertEqual(resolve_smart_menu_choice("invest"), "7")     # Keyword: invest -> wealth advisory
        self.assertEqual(resolve_smart_menu_choice("score"), "6")      # Keyword: score -> 50/30/20 scorecard
        self.assertEqual(resolve_smart_menu_choice("subs"), "9")       # Keyword: subs -> subscriptions
        self.assertEqual(resolve_smart_menu_choice("exitt"), "0")      # Typo: exitt -> exit
        self.assertIsNone(resolve_smart_menu_choice("random_garbage_xyz"))

        # Date normalization
        self.assertEqual(normalize_date_input("2026/10/05"), "2026-10-05")
        self.assertEqual(normalize_date_input("2026.10.05"), "2026-10-05")
        self.assertEqual(normalize_date_input("2026-1-5"), "2026-01-05")

        # Type & Currency Aliases
        self.assertEqual(TYPE_ALIASES["incom"], "income")
        self.assertEqual(TYPE_ALIASES["expnse"], "expense")
        self.assertEqual(CURRENCY_ALIASES["dollar"], "USD")
        self.assertEqual(CURRENCY_ALIASES["rupee"], "INR")
        self.assertEqual(CURRENCY_ALIASES["eruo"], "EUR")


    # -------------------------------------------------------------------------
    # ADVANCED FINTECH SERVICES: RUNWAY, TRENDS & JSON BACKUP TESTS
    # -------------------------------------------------------------------------
    def test_financial_runway_and_burn_velocity(self):
        """Verifies monthly burn rate, velocity, and emergency runway calculation."""
        # sample_transactions has ₹1370 expense in October
        runway = calculate_financial_runway(self.sample_transactions, 5000.0)
        self.assertEqual(runway["savings"], 5000.0)
        self.assertEqual(runway["monthly_burn"], 1370.0)
        self.assertAlmostEqual(runway["runway_months"], 3.6, places=1)
        self.assertIn("HEALTHY", runway["status"])

    def test_month_over_month_trend_analysis(self):
        """Verifies MoM trend calculations across chronological months."""
        extended_records = list(self.sample_transactions) + [
            {"id": 5, "date": "2026-11-02", "type": "expense", "category": "Food", "amount": 2000.0, "currency": "INR", "amount_inr": 2000.0}
        ]
        trends = analyze_monthly_trends(extended_records)
        self.assertEqual(len(trends), 2)
        self.assertEqual(trends[0]["month"], "2026-10")
        self.assertEqual(trends[1]["month"], "2026-11")
        # Oct exp was 1370, Nov exp is 2000 -> ((2000-1370)/1370)*100 = +46.0%
        self.assertGreater(trends[1]["delta_pct"], 0)
        self.assertIn("▲", trends[1]["direction"])

    def test_json_backup_export(self):
        """Verifies structured JSON export and metadata serialization."""
        import json
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as tmp:
            tmp_path = tmp.name

        try:
            out_file = export_json_backup(self.sample_transactions, filename=tmp_path)
            self.assertEqual(out_file, tmp_path)
            with open(tmp_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("metadata", data)
            self.assertEqual(data["metadata"]["total_records"], 4)
            self.assertEqual(len(data["transactions"]), 4)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
