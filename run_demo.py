"""
Automated Demonstration & Output Capture Script
Course: Computational Thinking and Programming (2026CSAE100)
Bennett University

Executes all core and advanced computational services non-interactively
and outputs formatted console captures for evaluation slides and reports.
"""

from main import (
    load_transactions,
    calculate_monthly_summary,
    analyze_50_30_20_health,
    generate_wealth_advisory,
    detect_expense_leaks_and_anomalies,
    analyze_recurring_subscriptions,
    convert_currency,
    export_monthly_report,
    CSV_FILE
)

def run_comprehensive_demo():
    print("=" * 70)
    print("  FINMATRICS — INTELLIGENT FINANCIAL ADVISORY SYSTEM")
    print("  Comprehensive Demonstration of All Features & Services")
    print("=" * 70)

    # 1. Load Data
    transactions = load_transactions(CSV_FILE)
    print(f"\n[DEMO] Successfully loaded {len(transactions)} transactions from {CSV_FILE}.")

    # 2. Multi-Currency Demo (Service A)
    print("\n" + "=" * 60)
    print("DEMO FEATURE 1: MULTI-CURRENCY CONVERSION ENGINE (Service A)")
    print("=" * 60)
    amount_usd = 15.0
    converted_inr = convert_currency(amount_usd, "USD", "INR")
    converted_eur = convert_currency(converted_inr, "INR", "EUR")
    print(f"Sample Currency Conversion:")
    print(f"  • ${amount_usd:.2f} USD = ₹{converted_inr:.2f} INR")
    print(f"  • ₹{converted_inr:.2f} INR = €{converted_eur:.2f} EUR")

    # 3. Monthly Summary for October 2026
    print("\n" + "=" * 60)
    print("DEMO FEATURE 2: MONTHLY SUMMARY (2026-10) [Core Aggregation]")
    print("=" * 60)
    summary = calculate_monthly_summary(transactions, "2026-10")
    print(f"Target Month:       {summary['month']}")
    print(f"Total Income:       ₹{summary['total_income']:.2f}")
    print(f"Total Expenses:     ₹{summary['total_expenses']:.2f}")
    print(f"Net Savings:        ₹{summary['balance']:.2f}")
    print(f"Transaction Count:  {summary['count']}")
    print("\nCategory Breakdown:")
    for cat in sorted(summary['categories'].keys()):
        amt = summary['categories'][cat]
        pct = (amt / summary['total_expenses'] * 100) if summary['total_expenses'] > 0 else 0
        print(f"  - {cat:<15}: ₹{amt:>8.2f} ({pct:5.1f}%)")
    highest_cat, highest_amt = summary['highest_category']
    print(f"\nHighest Spending Category: {highest_cat} (₹{highest_amt:.2f})")

    # 4. 50/30/20 Financial Health Scorecard (Service C)
    print("\n" + "=" * 60)
    print("DEMO FEATURE 3: 50/30/20 FINANCIAL HEALTH SCORECARD (Service C)")
    print("=" * 60)
    scorecard = analyze_50_30_20_health(transactions, "2026-10")
    print(f"Financial Health Score: {scorecard['score']} / 100 [{scorecard['grade']}]")
    print(f"  • Needs:   ₹{scorecard['needs_total']:.2f} [{scorecard['needs_pct']}%] (Target: <= 50%)")
    print(f"  • Wants:   ₹{scorecard['wants_total']:.2f} [{scorecard['wants_pct']}%] (Target: <= 30%)")
    print(f"  • Savings: ₹{scorecard['savings_total']:.2f} [{scorecard['savings_pct']}%] (Target: >= 20%)")
    print("Actionable Recommendations:")
    for idx, rec in enumerate(scorecard['recommendations'], 1):
        print(f"  {idx}. {rec}")

    # 5. Surplus Wealth Allocation & SIP Advisory (Service B)
    print("\n" + "=" * 60)
    print("DEMO FEATURE 4: SURPLUS WEALTH ALLOCATION & SIP ENGINE (Service B)")
    print("=" * 60)
    surplus = summary['balance']
    advisory = generate_wealth_advisory(surplus, "moderate")
    print(f"Unspent Capital (Surplus): ₹{surplus:.2f}")
    print(f"Risk Strategy: {advisory['profile']} (Index Investing & Emergency Shield)")
    print("Recommended Allocation:")
    for asset, amt in advisory['allocations'].items():
        pct = (amt / surplus * 100) if surplus > 0 else 0
        print(f"  • {asset:<40}: ₹{amt:>9.2f} ({pct:4.1f}%)")
    print("\nCompound SIP Growth Projection (@ 11.5% p.a.):")
    print(f"  • In 1 Year:  ₹{advisory['projections']['1_year']:>10.2f}")
    print(f"  • In 3 Years: ₹{advisory['projections']['3_years']:>10.2f}")
    print(f"  • In 5 Years: ₹{advisory['projections']['5_years']:>10.2f}")

    # 6. Expense Leak & Anomaly Detection (Service D)
    print("\n" + "=" * 60)
    print("DEMO FEATURE 5: EXPENSE LEAK & ANOMALY DETECTOR (Service D)")
    print("=" * 60)
    patterns = detect_expense_leaks_and_anomalies(transactions)
    print("Micro-Spending Habit Leaks:")
    if patterns["leaks"]:
        for leak in patterns["leaks"]:
            print(f"  • {leak['category']}: {leak['count']} transactions totaling ₹{leak['total_spent']:.2f}")
            print(f"    Annualized Drain: ₹{leak['annual_impact']:.2f}/year!")
    else:
        print("  None detected.")

    print("\nSpending Spikes / Anomalies:")
    if patterns["anomalies"]:
        for a in patterns["anomalies"]:
            print(f"  • [ID #{a['id']}] {a['date']} | {a['category']}: ₹{a['amount']:.2f} (Spike is {a['multiplier']}x baseline avg ₹{a['average']:.2f})")
    else:
        print("  No spikes detected.")

    # 7. Recurring Subscription Audit (Service F)
    print("\n" + "=" * 60)
    print("DEMO FEATURE 6: RECURRING SUBSCRIPTION & BILL SQUEEZE (Service F)")
    print("=" * 60)
    subs = analyze_recurring_subscriptions(transactions)
    print("Committed Recurring Subscriptions:")
    for name, amt in subs["subscriptions"].items():
        print(f"  • {name:<35}: ₹{amt:>8.2f}/mo (₹{(amt * 12):>9.2f}/yr)")
    print(f"Total Monthly Recurring Burn: ₹{subs['monthly_burn']:.2f}")
    print(f"Total Annual Committed Cost:  ₹{subs['annual_burn']:.2f}")

    # 8. Export Report
    print("\n" + "=" * 60)
    print("DEMO FEATURE 7: COMPREHENSIVE AUDIT REPORT EXPORT")
    print("=" * 60)
    export_monthly_report_demo(transactions, "2026-10")

    print("\n" + "=" * 70)
    print("  ALL DEMONSTRATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)

def export_monthly_report_demo(transactions, month_str):
    summary = calculate_monthly_summary(transactions, month_str)
    scorecard = analyze_50_30_20_health(transactions, month_str)
    advisory = generate_wealth_advisory(max(0.0, summary["balance"]), "moderate")
    subscriptions = analyze_recurring_subscriptions(transactions)
    report_filename = f"monthly_report_{month_str}.txt"

    with open(report_filename, "w", encoding="utf-8") as rep:
        rep.write("=" * 70 + "\n")
        rep.write(f"  COMPREHENSIVE FINANCIAL AUDIT & INTELLIGENT REPORT: {month_str}\n")
        rep.write("=" * 70 + "\n\n")
        rep.write("1. EXECUTIVE SUMMARY (BASE INR)\n")
        rep.write("-" * 40 + "\n")
        rep.write(f"Total Transactions: {summary['count']}\n")
        rep.write(f"Total Income:       ₹{summary['total_income']:.2f}\n")
        rep.write(f"Total Expenses:     ₹{summary['total_expenses']:.2f}\n")
        rep.write(f"Net Savings:        ₹{summary['balance']:.2f}\n\n")

        rep.write("2. CATEGORY BREAKDOWN\n")
        rep.write("-" * 40 + "\n")
        for cat in sorted(summary["categories"].keys()):
            amt = summary["categories"][cat]
            pct = (amt / summary["total_expenses"] * 100) if summary["total_expenses"] > 0 else 0
            rep.write(f"  - {cat:<18}: ₹{amt:>9.2f} ({pct:5.1f}%)\n")
        highest_cat, highest_amt = summary["highest_category"]
        rep.write(f"\nHighest Spending Category: {highest_cat} (₹{highest_amt:.2f})\n\n")

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

    print(f"Report exported successfully to: {report_filename}")

if __name__ == "__main__":
    run_comprehensive_demo()
