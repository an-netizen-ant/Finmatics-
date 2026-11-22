# FinMatrics — Intelligent Multi-Currency Expense Tracker & Financial Advisory System
### Computational Thinking and Programming (2026CSAE100) — Bennett University
**Academic Year:** 2026–27  
**Team Members:** Samriddhi Jain, Pranjaldeep Kaur, Ashu Kumar, Ansh Vardhan, Anant Gupta

---

## 📌 Project Overview
**FinMatrics** elevates traditional personal expense tracking into an intelligent, active computational financial advisor. Developed in pure Python using only standard library modules, it features:
- **Universal Multi-Currency Engine (Service A):** Offline-first conversion across 7 global currencies (`INR`, `USD`, `EUR`, `GBP`, `JPY`, `AED`, `CAD`).
- **Surplus Wealth Allocation & SIP Simulator (Service B):** Mathematically partitions unspent funds across Emergency Buffers, Index SIPs, and Upskilling funds, forecasting 1, 3, and 5-year compound growth ($FV$).
- **50/30/20 Financial Health Scorecard (Service C):** Automatically scores your spending ratio on a 0–100 scale (Needs $\le 50\%$, Wants $\le 30\%$, Savings $\ge 20\%$).
- **Expense Leak & Anomaly Detection (Service D):** Flags the annual drain of habitual micro-spending and identifies spending spikes $\ge 2\times$ category baseline averages.
- **Recurring Subscription Squeeze Detector (Service F):** Audits recurring monthly commitments (streaming, utilities, software) and calculates total annual fixed burn.
- **Crash-Proof CSV Persistence:** Self-healing file loader with automatic schema backward compatibility.
- **Formal Unit Testing Suite:** 12 automated test cases with 100% pass rate.

---

## 📂 Repository Structure

```text
├── main.py                     # Main interactive application entry point (18 functions)
├── transactions.csv            # Persistent CSV data storage with multi-currency & recurring flags
├── test_expense_tracker.py     # 12-test automated unit & integration test suite (unittest)
├── run_demo.py                 # Automated demonstration script for output captures
├── monthly_report_2026-10.txt  # Sample comprehensive financial audit report
├── PROJECT_REPORT_FINAL.md     # Complete project report covering all 10 required sections
├── VIVA_GUIDE.md               # Comprehensive viva voce preparation guide for all 5 members
└── README.md                   # Project documentation & run guide
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.8+ (Zero external dependencies; uses only `csv`, `datetime`, `math`, `pathlib`, `typing`, `unittest`).

### 1. Run the Interactive Application
```bash
python3 main.py
```

### 2. Run the Automated Test Suite (12 Tests)
```bash
python3 test_expense_tracker.py
```
Expected output:
```text
............
----------------------------------------------------------------------
Ran 12 tests in 0.005s

OK
```

### 3. Run the Automated Demonstration Script
```bash
python3 run_demo.py
```

---

## 💡 Core Features & Computational Capabilities

1. **Add Transaction (Multi-Currency & Recurring Tag):** Records transactions in any supported currency, tags recurring subscriptions, and automatically normalizes to base INR.
2. **View Transactions:** Interactive table with option to view amounts in native currency or converted to any target currency.
3. **Monthly Summary:** Computes total income, expenses, savings, and category breakdown with dynamic $\arg\max$ ranking.
4. **Budget Check & Alerts:** Evaluates spending against monthly budget with 85% caution and 100% breach alerts.
5. **50/30/20 Financial Health Scorecard:** Mathematical scoring (0–100) based on personal finance principles.
6. **Surplus Wealth Allocation & SIP Advisory:** Algorithmic capital allocation with compound interest projections ($FV = P \times [\frac{(1+r)^n - 1}{r}] \times (1+r)$).
7. **Expense Leak & Anomaly Detector:** Identifies the "Latte Factor" / micro-spending drains and statistical category spikes.
8. **Recurring Subscription Audit:** Tracks recurring bills and calculates annual financial commitments.
9. **Multi-Currency Quick Converter:** Instant offline calculator between supported currencies.
10. **Comprehensive Audit Export:** Exports structured `.txt` report containing summaries, scorecards, advisory allocations, and transaction tables.

---

## 👥 Team Responsibilities

- **Samriddhi Jain (S26CSEU1985):** Menu design, defensive input validation, 50/30/20 Financial Health Scoring Engine.
- **Pranjaldeep Kaur (S26CSEU1934):** Crash-proof CSV storage architecture, backward-compatible schema migration, Multi-Currency Conversion Engine.
- **Ashu Kumar (S26CSEU1963):** Core monthly summary aggregator, Surplus Wealth Allocation Advisor, SIP Compounding Simulator.
- **Ansh Vardhan (S26CSEU1919):** Expense Leak & Anomaly Detection, Recurring Subscription Squeeze Detector, 12-test automated unit test suite.
- **Anant Gupta (S26CSEU1940):** Comprehensive Audit Report generator, integration testing, code optimization, and documentation.

---

## 📖 Evaluation & Viva Preparation
Review the included **`VIVA_GUIDE.md`** file for:
- Member-specific question sets and code walkthroughs.
- Detailed explanations of all algorithms (SIP compounding, 50/30/20 scoring, anomaly detection, currency conversion).
- Common live code modification challenges with ready-to-run solutions.
