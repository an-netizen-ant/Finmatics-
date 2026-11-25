# FinMatrics — Intelligent Multi-Currency Expense Tracker & Financial Advisory System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-16%20passed-brightgreen.svg)](test_expense_tracker.py)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Standard%20Library)-orange.svg)](#architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent, crash-proof personal finance management and advisory console system built for university students and young professionals. Developed for **Computational Thinking and Programming (2026CSAE100)** at **Bennett University**.

---

## 📌 Why FinMatrics?
Most student expense trackers are passive number loggers that crash as soon as a user enters a typo or non-numeric amount. 

**FinMatrics** transforms personal finance from passive logging into an **intelligent advisory dashboard**. It actively warns you about spending spikes, audits recurring subscriptions, calculates your financial runway, scores your budget discipline using the 50/30/20 rule, and simulates compound investment growth for your leftover money — all offline, right in your terminal, with **zero external dependencies**.

---

## 👥 Team Members & Collaborative Division of Work

| Team Member | Enrollment No. | Core Modules & Ownership |
|---|---|---|
| **Samriddhi Jain** | S26CSEU1985 | Input validation layer, fuzzy typo resolution, and 50/30/20 scoring engine |
| **Pranjaldeep Kaur** | S26CSEU1934 | Fault-tolerant CSV persistence layer, backward schema compatibility, and multi-currency matrix |
| **Ashu Kumar** | S26CSEU1963 | Monthly summary engine, surplus wealth advisory, and compound SIP simulator |
| **Ansh Vardhan** | S26CSEU1919 | Statistical anomaly detection, micro-leak tracking, subscription squeeze, and unit test suite |
| **Anant Gupta** | S26CSEU1940 | Financial runway engine, MoM trend analysis, JSON backup, audit report export, and integration |

---

## 💡 Key Features & Capabilities

### 1. Multi-Currency Engine (Service A)
- Support for **7 global currencies**: INR (₹), USD ($), EUR (€), GBP (£), JPY (¥), AED (AED), and CAD (C$).
- Offline exchange rate peg matrix with automatic normalization to base INR.
- Interactive multi-currency converter utility.

### 2. Defensive Input & Smart Typo Assistant
- Uses `difflib.get_close_matches` for intelligent fuzzy matching:
  - Menu keywords: Typing `sumary` routes to `3`, `invest` routes to `7`, `subs` routes to `9`.
  - Type & currency aliases: `usdd` $\to$ `USD`, `expnse` $\to$ `expense`, `rupee` $\to$ `INR`.
  - Date normalization: Auto-formats `2026/10/05` or `2026.10.5` into valid `2026-10-05`.
- Defensive `try...except ValueError` loops ensure the program never crashes on wrong inputs.

### 3. 50/30/20 Financial Health Scorecard (Service C)
- Categorizes spending into **Needs (≤ 50%)**, **Wants (≤ 30%)**, and **Savings (≥ 20%)** using constant-time $O(1)$ set lookups.
- Computes an algorithmic financial health score (0–100) and awards letter grades from **A+ to F** with actionable coaching tips.

### 4. Surplus Wealth Advisory & SIP Simulator (Service B)
- Recommends tailored asset allocations for unspent savings across 3 risk horizons:
  - **Conservative:** Emergency Buffer (50%), Safe RD/Debt (30%), Upskilling (20%).
  - **Moderate:** Nifty 50 Index SIP (50%), Emergency Fund (30%), Books & Courses (20%).
  - **Growth:** Diversified Equity (65%), Certifications (20%), Liquid Buffer (15%).
- Simulates 1, 3, and 5-year future compound returns using the financial annuity-due formula:
  $$FV = P \times \left[ \frac{(1 + r)^n - 1}{r} \right] \times (1 + r)$$

### 5. Expense Leak & Statistical Anomaly Detector (Service D)
- **Micro-Spending Habit Leaks:** Scans for small transactions ($\le ₹250$) in casual categories (Snacks, Canteen, Food) and computes the annual drain (e.g., daily ₹70 coffee habit = ₹25,200/year).
- **Spending Spikes (> 2x Category Average):** Uses **Leave-One-Out** baseline averaging so large spikes don't inflate the threshold.

### 6. Recurring Subscription & Bill Squeeze Detector (Service F)
- Audits monthly recurring commitments (Netflix, Spotify, broadband, utilities).
- Computes **Monthly Burn** and **Annual Committed Cost**, showing how pausing unused services frees capital for savings.

### 7. Financial Runway & Cashflow Velocity Calculator (Service G) *(New)*
- Computes your **Average Monthly Burn Rate** and **Daily Spending Velocity**.
- Projects your **Financial Survival Runway** in months based on current liquid bank reserves ($Runway = \frac{Reserves}{Monthly Burn}$).
- Evaluates safety tiers from **FORTRESS (6+ months)** to **CRITICAL (< 1 month)**, providing a recommended safe daily spending pace.

### 8. Month-over-Month (MoM) Trend & Variance Analysis (Service H) *(New)*
- Chronological spending variance deltas across recorded months.
- Directional spending trajectory indicators (`▲ +18.4%` vs `▼ -6.2%`).

### 9. Visual ASCII Horizontal Bar Charts *(New)*
- Renders clean horizontal bar charts directly in your terminal for monthly category distributions:
  ```text
  Food           | ████████████████████ |  32.8% (₹  450.00)
  Transport      | █████                |   8.8% (₹  120.00)
  Education      | ████████████████████ |  58.4% (₹  800.00)
  ```

### 10. Data Portability & Audit Dossiers (Service I)
- **CSV Storage:** Dual-mode CSV loader supports both modern and legacy schemas with automatic recovery.
- **JSON Ledger Backup:** Complete versioned ledger backup (`backup_ledger_YYYYMMDD.json`) with metadata and record checksums.
- **Audit Reports:** Generates formatted text dossiers (`monthly_report_YYYY-MM.txt`) with aligned ASCII tables.

---

## 🛠️ System Architecture

```text
+--------------------------------------------------------------------------+
|                       USER INTERACTION & MENU LOOP                       |
|           (difflib Typo Assistant • 14 Options • Natural Keywords)       |
+--------------------------------------------------------------------------+
      |                  |                    |                  |
      v                  v                    v                  v
+----------------+ +---------------+ +------------------+ +-----------------+
| VALIDATION     | | CSV STORAGE   | | ANALYTICS ENGINE | | ADVISORY ENGINE |
| (Samriddhi)    | | (Pranjaldeep) | | (Ashu & Ansh)    | | (Anant & Team)  |
|                | |               | |                  | |                 |
| • Fuzzy Type   | | • DictReader  | | • Monthly Totals | | • 50/30/20      |
| • Date Normal. | | • Positional  | | • ASCII Charts   | | • Wealth / SIP  |
| • Currency Peg | | • Next ID Gen | | • Anomaly Spike  | | • Runway Calc   |
| • Float Guards | | • Auto-Repair | | • Subscription   | | • MoM Trends    |
+----------------+ +---------------+ +------------------+ +-----------------+
                                              |
                                              v
                              +--------------------------------+
                              |    REPORTING & DATA BACKUP     |
                              | • Text Audit Report (.txt)     |
                              | • Versioned JSON Backup (.json)|
                              +--------------------------------+
```

---

## 📂 Repository Structure

```text
├── main.py                     # FinMatrics Pro Application (~1,500 lines)
├── main_simple.py              # Lightweight Syllabus-Compliant Version
├── transactions.csv            # Persistent multi-currency CSV ledger
├── test_expense_tracker.py     # Comprehensive automated test suite (16 tests)
├── test_expense_tracker_simple.py # Test suite for lightweight version (8 tests)
└── README.md                   # Project documentation & architecture guide
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher.
- No third-party packages needed (`pip install` is NOT required).

### Running FinMatrics
```bash
# Run the complete feature-rich application
python3 main.py

# Or run the lightweight syllabus-compliant version
python3 main_simple.py
```

### Running Automated Tests
```bash
# Run the full 16-test suite
python3 test_expense_tracker.py

# Or run the 8-test simple suite
python3 test_expense_tracker_simple.py
```

---

## 🧪 Automated Test Suite (16/16 Passing)

The test suite covers:
1. `test_case_1_add_expense`: Add expense and auto-generate ID.
2. `test_case_2_monthly_summary_calculation`: Monthly aggregation verification.
3. `test_case_3_highest_spending_category`: Identification of max expenditure category.
4. `test_case_4_budget_calculation`: Budget subtraction and threshold detection.
5. `test_case_5_input_validation`: Leap year and calendar date guards.
6. `test_currency_conversion_accuracy_and_crash_proof`: 7-currency conversion matrix.
7. `test_sip_compounding_future_value_formula`: Compound interest annuity-due math.
8. `test_wealth_advisory_profiles`: Asset partitioning across risk profiles.
9. `test_50_30_20_scoring_logic`: Algorithmic financial score and bounds.
10. `test_expense_leak_and_anomaly_detection`: Micro-spends and leave-one-out outlier detection.
11. `test_recurring_subscriptions_detection`: Monthly and annual recurring burn.
12. `test_csv_backward_compatibility_and_persistence`: Legacy CSV column fallback.
13. `test_smart_typo_resolution`: `difflib` keyword and spelling corrections.
14. `test_financial_runway_and_burn_velocity`: Daily velocity and survival runway.
15. `test_month_over_month_trend_analysis`: Chronological variance deltas.
16. `test_json_backup_export`: JSON serialization and metadata integrity.

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
