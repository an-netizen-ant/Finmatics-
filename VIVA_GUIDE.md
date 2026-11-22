# Comprehensive Viva Voce Preparation Guide (Updated)
## Python Expense Tracker & Intelligent Financial Advisory System
### Computational Thinking and Programming (2026CSAE100) — Bennett University

---

## 1. General Project Overview (All 5 Members Must Know)

### Q1: What makes your project distinct from other student expense trackers?
**Answer:** While standard student projects only record and print numbers, our project functions as an **Intelligent Financial Advisory System**:
1. **Multi-Currency Support (Service A):** Offline conversion matrix across 7 global currencies (INR, USD, EUR, GBP, JPY, AED, CAD) with automatic base normalization to INR.
2. **Surplus Wealth Allocation & SIP Compounding (Service B):** Mathematically advises users on investing unspent budget into Emergency Funds, Index SIPs, and Upskilling, projecting 1, 3, and 5-year compound growth using the actual compounding formula.
3. **50/30/20 Financial Health Scorecard (Service C):** Computes an algorithmic score (0–100) evaluating Needs, Wants, and Savings distribution.
4. **Expense Leak & Outlier Detection (Service D):** Flags the cumulative annual impact of small micro-spending habits (e.g., ₹70 daily snacks = ₹25,200/year) and detects spending spikes $\ge 2\times$ category average.
5. **Recurring Subscription Audit (Service F):** Detects monthly recurring commitments and calculates annual fixed burn.
6. **Zero External Dependencies & Zero-Crash Architecture:** Runs entirely on Python standard library modules (`csv`, `datetime`, `math`, `pathlib`).

### Q2: How does the application prevent runtime crashes?
**Answer:**
1. **Calendar Validation:** Uses `datetime.strptime()` to reject non-existent calendar dates (e.g., `2026-02-29` on non-leap years).
2. **Safe Float Conversions:** Uses `while True` with `try-except ValueError` and explicit `amount > 0` checks.
3. **Division by Zero Guards:** In percentage calculations and scorecard evaluations, every denominator has a guard: `pct = (val / total * 100) if total > 0 else 0.0`.
4. **CSV Fault Tolerance:** In `load_transactions()`, malformed rows or missing columns default to safe values (`currency="INR"`, `is_recurring=False`) rather than crashing the program.

---

## 2. Member-Specific Viva Questions & Explanations

### 2.1 Samriddhi Jain (Enrollment: S26CSEU1985)
**Role:** Defensive Input Validation, Interactive Menu Dispatch, and 50/30/20 Financial Health Scoring Engine.

#### Q1: Explain the mathematical logic behind your 50/30/20 scoring algorithm.
**Explanation:** 
- The score starts at a baseline of $100.0$ points.
- If spending on **Needs** exceeds the $50\%$ target, we deduct points proportionally: $\min(40.0, (\text{Needs}\% - 50.0) \times 1.5)$.
- If spending on **Wants** exceeds the $30\%$ target, we deduct: $\min(40.0, (\text{Wants}\% - 30.0) \times 2.0)$.
- If **Savings** falls below the $20\%$ target, we deduct: $\min(40.0, (20.0 - \text{Savings}\%) \times 2.0)$.
- The final score is bounded using $\max(0.0, \min(100.0, \text{score}))$. Grades are assigned as A (85–100), B (70–84), C (50–69), and D (<50).

#### Q2: How do you categorize transactions into Needs, Wants, and Savings?
**Explanation:** We use pre-defined Python sets (`NEEDS_CATEGORIES`, `WANTS_CATEGORIES`, `SAVINGS_CATEGORIES`) for $O(1)$ constant-time lookup. When an expense is recorded, `cat.strip().lower()` is checked against these sets. Any unclassified category defaults safely to "Needs" so we never underestimate essential living costs.

---

### 2.2 Pranjaldeep Kaur (Enrollment: S26CSEU1934)
**Role:** CSV Storage Architecture, Backward Compatibility, and Multi-Currency Conversion Engine.

#### Q1: How does the Multi-Currency Conversion Engine work without internet access?
**Explanation:** We utilize an offline exchange rate matrix `EXCHANGE_RATES` pegged to 1 INR (Base currency):
```python
def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    amount_in_inr = amount / EXCHANGE_RATES[from_curr]
    converted = amount_in_inr * EXCHANGE_RATES[to_curr]
    return round(converted, 2)
```
To convert from any currency $A$ to currency $B$, we first normalize to INR by dividing by $A$'s rate, and then multiply by $B$'s rate. If an unrecognized currency is passed, it returns the original amount without crashing.

#### Q2: What is "Backward Compatibility" in your CSV loader?
**Explanation:** In `load_transactions()`, we use `row.get("currency", "INR")` and `row.get("is_recurring", "no")`. If the user loads an older CSV file created before multi-currency support was added, the program automatically supplies default values instead of throwing a `KeyError`.

---

### 2.3 Ashu Kumar (Enrollment: S26CSEU1963)
**Role:** Monthly Summaries, Surplus Wealth Allocation Advisor, and SIP Compounding Engine.

#### Q1: What is the formula for the SIP Future Value calculation, and how did you implement it?
**Explanation:** 
$$FV = P \times \left[ \frac{(1 + r)^n - 1}{r} \right] \times (1 + r)$$
Where:
- $P$ is the monthly investment amount.
- $r$ is the periodic monthly interest rate: $(\text{annual\_rate} / 100) / 12$.
- $n$ is total months: $\text{years} \times 12$.
In Python:
```python
r = (annual_return_rate / 100) / 12
n = years * 12
fv = monthly_investment * (((math.pow(1 + r, n) - 1) / r) * (1 + r))
```

#### Q2: How does the Wealth Advisory service recommend different asset allocations?
**Explanation:** It offers three distinct risk profiles:
1. **Conservative:** 50% High-Yield Emergency Buffer, 30% Safe Recurring Deposit/Debt, 20% Skill Development.
2. **Moderate (Default):** 50% Nifty 50 Index Fund SIP, 30% Emergency Cushion, 20% Books & Upskilling.
3. **Growth:** 65% Diversified Equity SIP, 20% Tech Upskilling/Certifications, 15% Emergency Buffer.

---

### 2.4 Ansh Vardhan (Enrollment: S26CSEU1919)
**Role:** Expense Leak & Anomaly Detection, Recurring Subscription Squeeze, and Automated Test Suite.

#### Q1: How does the program detect "Expense Leaks"?
**Explanation:** It scans for transactions with amount $\le ₹250$ in casual categories (Snacks, Food, Canteen). If $\ge 3$ such transactions exist in a category, it groups them and projects the annualized cost: $\text{Annual Drain} = \text{Total Spent} \times 12$. This demonstrates to the user how a small daily ₹70 coffee or snack habit drains over ₹25,000 annually.

#### Q2: How does the program detect unusual spending spikes (anomalies)?
**Explanation:** For each expense transaction $t_i$, it computes the baseline average of *all other* transactions in that same category:
$$\text{baseline\_avg} = \frac{\sum_{j \ne i} t_j}{\text{count} - 1}$$
If $t_i \ge 2.0 \times \text{baseline\_avg}$ and $t_i \ge ₹500$, it is flagged as an anomaly.

#### Q3: How is the Recurring Subscription Squeeze calculated?
**Explanation:** It extracts all expenses marked `is_recurring=True` (e.g. Netflix, Spotify, Broadband). It sums them to get `Monthly Burn`, multiplies by 12 for `Annual Burn`, and presents actionable advice on how much savings would be redirected to investments by canceling unused subscriptions.

---

### 2.5 Anant Gupta (Enrollment: S26CSEU1940)
**Role:** Comprehensive Audit Report Export, Integration, Code Optimization, and Defensive Verification.

#### Q1: What information is included in `monthly_report_YYYY-MM.txt`?
**Explanation:** The exported audit report compiles data from all modules:
1. Executive Summary (Income, Expenses, Net Savings in base INR).
2. Category Breakdown with percentage shares and highest spending category.
3. 50/30/20 Financial Health Score and breakdown.
4. Surplus Wealth Allocation recommendations and 5-year SIP forecast.
5. Recurring Subscriptions monthly/annual burn audit.
6. Formatted table of all transactions for the month.

#### Q2: Why is `math.pow()` used instead of `**` in some calculations?
**Explanation:** `math.pow(x, y)` converts its arguments to floating-point numbers and uses the C math library under the hood, ensuring predictable IEEE 754 float precision across platforms. Both `**` and `math.pow()` are valid, but `math.pow()` clearly documents intentional floating-point power operations in financial formulas.

---

## 3. Top Expected Code Modification Questions (Live Coding in Viva)

### Mod 1: "Add a new supported currency, e.g., Australian Dollar (AUD)."
**Answer:** In `main.py`, simply add `AUD` to `EXCHANGE_RATES` and `CURRENCY_SYMBOLS`:
```python
EXCHANGE_RATES["AUD"] = 0.018   # 1 INR = 0.018 AUD
CURRENCY_SYMBOLS["AUD"] = "A$"
```
Because the currency engine uses dictionary lookups, it immediately supports conversions to and from AUD without changing any other function!

### Mod 2: "Filter transactions by date range (start_date to end_date)."
```python
def filter_by_date_range(transactions, start_date, end_date):
    return [t for t in transactions if start_date <= t["date"] <= end_date]
```

### Mod 3: "Change the threshold for micro-spending leaks from ₹250 to ₹150."
In `detect_expense_leaks_and_anomalies()`, change:
```python
if t["amount_inr"] <= 150.0:
```

### Mod 4: "Add an extra 10-year projection in the SIP simulator."
In `generate_wealth_advisory()`, add:
```python
"10_years": calculate_sip_future_value(invest_amt, exp_return, 10)
```
