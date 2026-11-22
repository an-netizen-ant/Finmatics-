"""
Simulates an end-to-end interactive CLI session through stdin piping,
testing all 12 menu options, bad inputs, recovery, and clean exit.
"""

import subprocess
import sys

def test_full_cli_session():
    # Sequence of user keystrokes:
    inputs = [
        # 1. Invalid menu choice (testing menu crash-resistance)
        "99",
        "abc",
        "",

        # 2. Add Transaction (Option 1) with intentional bad inputs first
        "1",
        "invalid-date",      # Bad date
        "2026-02-29",        # Non-leap year bad date
        "2026-10-25",        # Valid date
        "bad-type",          # Bad type
        "expense",           # Valid type
        "",                  # Blank category
        "Books",             # Valid category
        "-50",               # Negative amount
        "not_a_number",      # Bad amount
        "350",               # Valid amount
        "bad_currency",      # Unsupported currency
        "INR",               # Valid currency
        "Algorithms textbook", # Description
        "y",                 # Recurring? Yes

        # 3. View Transactions (Option 2)
        "2",
        "USD",               # View in USD

        # 4. View Transactions again in native
        "2",
        "",                  # Blank for native

        # 5. Monthly Summary (Option 3)
        "3",
        "2026-10",           # Valid month
        "INR",               # Summary currency

        # 6. Budget Check (Option 4)
        "4",
        "2026-10",           # Valid month
        "10000",             # Budget amount

        # 7. 50/30/20 Scorecard (Option 6)
        "6",
        "2026-10",

        # 8. Surplus Wealth Advisory (Option 7)
        "7",
        "2026-10",
        "2",                 # Moderate profile

        # 9. Expense Leak & Anomaly Detection (Option 8)
        "8",

        # 10. Recurring Subscriptions Audit (Option 9)
        "9",

        # 11. Currency Converter (Option 10)
        "10",
        "USD",
        "INR",
        "50",

        # 12. Export Report (Option 11)
        "11",
        "2026-10",

        # 13. Delete Transaction (Option 5)
        "5",
        "not_an_id",         # Bad ID
        "9999",              # Non-existent ID
        "5",
        "c",                 # Cancel deletion
        
        # 14. Clean Exit (Option 0)
        "0"
    ]

    simulated_input = "\n".join(inputs) + "\n"

    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(input=simulated_input, timeout=10)

    print("Subprocess Exit Code:", proc.returncode)
    if proc.returncode != 0:
        print("STDERR OUTPUT:\n", stderr)
        sys.exit(1)

    # Check that no Python Traceback or Unhandled Exception occurred
    if "Traceback" in stderr or "Traceback" in stdout:
        print("TRACEBACK DETECTED!\n", stdout, stderr)
        sys.exit(1)

    print("CLI Interaction Test: ALL 12 MENU OPTIONS & INPUT TRAPS PASSED CLEANLY!")
    assert "Thank you for using Python Expense Tracker & Financial Advisor. Goodbye!" in stdout

if __name__ == "__main__":
    test_full_cli_session()
