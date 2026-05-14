---
name: tax-audit-3cd
description: >
  Assist with Income Tax Audit under Section 44AB. Covers Form 3CA/3CB (audit report)
  and Form 3CD clause-by-clause (44 clauses). Guides the CA through each clause,
  collects relevant information from Tally/books, drafts disclosure remarks, and
  checks for common disallowances. Applicable for business turnover > Rs.1 Cr and
  professional receipts > Rs.50 Lakh.
when_to_use: >
  When preparing Form 3CA/3CB + 3CD for a client's tax audit. For each clause of
  3CD, ask the relevant questions and draft disclosures. Also for reviewing a
  completed 3CD before signing.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - mcp__tally__get_ledger_report
  - Read
  - Write
---

# Form 3CA / 3CB + 3CD — Tax Audit

**FINANCIAL INTEGRITY**: Form 3CD is a statutory certificate under Section 44AB. The auditing CA is personally responsible for the accuracy of each clause. Never certify a clause without reviewing the underlying documents. Incorrect certification can lead to penalty u/s 271B.

## Form Selection

| Situation | Form |
|---|---|
| Accounts maintained as per Companies Act | 3CA |
| Accounts NOT maintained under Companies Act (firms, individuals, etc.) | 3CB |
Both situations: Form 3CD is the same

## Form 3CB Draft

Generate Form 3CB:
```
FORM NO. 3CB
[Under Section 44AB of the Income-tax Act, 1961]

I/We [CA Name], Chartered Accountant, having Membership No. [XXXXXX], partner/proprietor
of M/s [Firm Name] (ICAI Firm Reg. No. [XXXXXX]), have examined the accounts and records
of [Business Name], [Address], Permanent Account Number [PAN], for the year ended 31st March [XXXX].

The financial statements, viz., the Profit and Loss Account for the year ended 31st March
[XXXX] showing a net profit/loss of Rs.[X] and the Balance Sheet as on 31st March [XXXX]
showing total assets of Rs.[X], are in agreement with the books of account maintained at
the above address.

[Standard 3CB paragraphs as per prescribed format]

Place: [City]  
Date: [Date]
[CA Signature + Membership No. + Firm Name + Reg No.]
```

## Form 3CD — Clause-by-Clause Guide

Work through each of the 44 clauses interactively:

### CLAUSE 1-4 — Basic Information
1. Name and address of the assessee
2. PAN
3. Status (Individual / HUF / Firm / AOP / Company / LLP / Trust)
4. Previous year ended: 31 March [XXXX] | AY: [AY]

### CLAUSE 5 — Whether liable to pay indirect taxes
Confirm: GST registration, GSTIN, turnover as per GST returns.
Disclose any GST audit findings, interest, or penalty paid during the year.

### CLAUSE 9 — Whether books of account prescribed under Section 44AA maintained
Specify books maintained: Cash Book, Ledger, Journal, Purchase/Sales Register, Vouchers.
For computerised accounts: specify software (Tally Prime, SAP, Zoho, etc.).

### CLAUSE 12 — Presumptive income (if applicable)
If Section 44AD/44ADA/44AE applies, state turnover and declared profit %.

### CLAUSE 14 — Method of Accounting
State: Mercantile / Cash basis. Any change in method during the year?

### CLAUSE 16 — Amounts debited to P&L (disallowances)
Critical clause — pull from Tally:
- 16(a) Capital expenditure charged to revenue (IT, furniture capitalised?)
- 16(b) Personal expenditure mixed with business
- 16(c) Advertisement or CSR expenditure if non-deductible

### CLAUSE 17 — Expenditure in the nature of capital
Identify any expense that should be capitalised but was expensed.

### CLAUSE 18 — Deductions under Sections 32/35/36/37
- Section 32: Depreciation schedule — WDV method (WDV opening + additions - disposals × depreciation rate)
- Section 35: Scientific research expenditure (35(1)(i) / 35(1)(ii) / 35(2AB))
- Section 36: Bad debts written off — list bad debts and confirm they were previously recognised as income
- Section 37: General business expenditure — confirm business purpose

### CLAUSE 19 — Amounts admissible under Sections 33AB/33ABA/35D/35DD/35DDA
Tea/Coffee/Rubber Board deposits, site restoration funds, amortised preliminary expenses.

### CLAUSE 21 — Amounts payable under Section 43B (Cash Basis Disallowances)
**CRITICAL**: These amounts are ONLY deductible in the year of actual payment.
- (a) Taxes, duties, cesses paid after 31 March (due date)
- (b) Employees' PF/ESI/Gratuity — paid to funds
- (c) Bonus/commission to employees
- (d) Interest on borrowings from financial institutions
- (e) Leave encashment

Pull from Tally: Outstanding provisions for above as on 31 March.
```
Section 43B Disallowances:
  Outstanding PF/ESI as on 31 Mar [XXXX]:         Rs.X [Disallowed if not paid by due date]
  Outstanding salary TDS:                         Rs.X
  Bonus payable (not yet paid):                   Rs.X
  Interest accrued on MSME dues (Section 43B(h)): Rs.X [NEW — from FY 2023-24]
Total 43B Disallowance:                           Rs.X
```

### CLAUSE 21(h) — Section 43B(h) — MSME Payment Compliance (NEW from FY 2023-24)
Any amount owed to MSME registered suppliers that was NOT paid within:
- 15 days (if no agreement) or agreed credit period (max 45 days)
is disallowed in the year of accrual and allowed only when paid.

Ask: "Do you have any MSME registered suppliers? If yes, list all outstanding payables."

### CLAUSE 22 — Payments in cash exceeding Rs.10,000 (Section 40A(3))
Pull from Tally: all cash payment vouchers > Rs.10,000 in a day to a single person.
```
Section 40A(3) Disallowances:
  Date | Payee | Amount | Nature | Disallowed?
  [list all cash payments > Rs.10,000]
```
Exception: Payments to banks, RBI, government, etc.

### CLAUSE 26 — Details of Speculation and Other Losses
- Speculation losses (commodity trading, derivatives)
- Deemed speculation (section 73)
- Set-off restrictions

### CLAUSE 30 — Details of TDS/TCS Compliances
- Transactions on which TDS applicable
- TDS deducted vs required
- Any default: late deduction / short deduction / non-deduction
- PAN not furnished — 20% TDS applied?
- Challan details

### CLAUSE 34 — Details of Specified Domestic Transactions (SDT) — Section 92BA
If SDT > Rs.20 Crore: Transfer pricing documentation (Form 3CEB required).

### CLAUSE 36 — Loans and Deposits received/repaid in cash
Section 269SS / 269T violations:
- Any cash loan/deposit received ≥ Rs.20,000 from a single person
- Any cash repayment ≥ Rs.20,000

### CLAUSE 41 — Demand raised / refund issued during the year
List all: Income Tax / GST / Custom / Other departmental demands during the year.

### CLAUSE 44 — Break-up of expenditure in respect of supplies received
From GSTN registered vs unregistered vs exempt/nil rated persons.
For firms with turnover > Rs.5 Crore: mandatory disclosure.

## Common Issues to Check Before Certification

```
PRE-CERTIFICATION CHECKLIST:
[ ] Books closed properly — no journal entries after trial balance date
[ ] Depreciation schedule reconciles with fixed asset register
[ ] All 43B items verified — PF/ESI/TDS paid before 31 March (or by due date)
[ ] MSME outstanding payments calculated (Section 43B(h))
[ ] Cash payment register reviewed — all Rs.10,000+ entries justified
[ ] TDS compliance: no defaults in deduction or payment
[ ] Any demand or notice during the year — disclosed in Clause 41
[ ] Audit report signed before 30 September of AY
```
