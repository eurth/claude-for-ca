---
name: caro-review
description: >
  Clause-by-clause review of CARO 2020 (Companies Auditor's Report Order 2020).
  Covers all 21 clauses — fixed assets, inventory, loans, compliance, fraud, related
  parties, internal controls, and more. Generates draft reporting format for each clause.
  Identifies which clauses need "adverse remarks" and helps draft qualified paragraphs.
when_to_use: >
  When auditing a company (other than CARO-exempt entities). After collecting working
  papers, use this to draft the CARO 2020 report to be appended to the audit report.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# CARO 2020 — Companies Auditor's Report Order

**FINANCIAL INTEGRITY**: CARO 2020 is mandatory for companies (except CARO-exempt). Any adverse remark has significant implications for the company. Every clause answer must be supported by audit evidence in the working papers. Unverified facts must not be stated.

## CARO 2020 Applicability

**EXEMPT from CARO 2020:**
- Banking, insurance, Section 8 companies
- Private limited companies with:
  - Paid-up capital + reserves ≤ Rs.1 crore, AND
  - Total borrowings ≤ Rs.1 crore (all types), AND
  - Total revenue ≤ Rs.10 crore
- One Person Companies (OPCs)

**APPLIES TO:**
All other companies, including listed, public, and private companies exceeding any of the above thresholds.

---

## CLAUSE-BY-CLAUSE TEMPLATE

Provide information for each clause and I will draft the reporting language.

---

### Clause (i) — Tangible Assets (Fixed Assets / Right-of-Use Assets)

**Required information:**
- Does the company maintain proper records showing full particulars (quantitative details + situation)?
- Has the company conducted physical verification of fixed assets at reasonable intervals?
- Are discrepancies material? If yes — what is the nature and treatment?
- Has the company revalued any assets? If yes — details of revaluation.
- Are any proceedings pending under Benami Property Transactions Act, 1988?

```
DRAFT CARO REPORTING — Clause (i):
(a) The company has maintained proper records showing full particulars, including quantitative details and situation of fixed assets/right-of-use assets.
(b) The fixed assets/right-of-use assets were physically verified by the management during the year. According to information and explanations given to us, no material discrepancies were noticed on such verification.
(c) The title deeds of immovable properties are held in the name of the company [EXCEPT: specify any exceptions].
(d) The company has not revalued its fixed assets/right-of-use assets during the year [OR: revaluation done by registered valuer; details appended].
(e) No proceedings have been initiated or pending against the company for holding any benami property under the Benami Transactions (Prohibition) Act, 1988.
```

---

### Clause (ii) — Inventory / Loans Against Security of Inventories

**Required information:**
- Physical verification of inventory — frequency, date of last verification
- Material discrepancies found?
- Outstanding against borrowings secured by pledge of inventories older than 90 days?

---

### Clause (iii) — Investments / Loans / Advances / Guarantees to Subsidiaries / Associates

**Required information:**
- Has the company made investments in, or given loans/guarantees to subsidiaries/associates/JVs?
- Are such investments/loans in accordance with Section 186?
- Terms and conditions not prejudicial to company's interest?
- Demand for repayment of overdue loans?

---

### Clause (iv) — Section 185 / 186 Compliance

**Required information:**
- Loans to directors u/s 185?
- Investments / guarantees / securities u/s 186?
- All approvals obtained?

---

### Clause (v) — Public Deposits (Section 73-76)

**Required information:**
- Has company accepted deposits from the public?
- If yes: Did it comply with Sections 73-76, Companies (Acceptance of Deposits) Rules?
- Any order from CLB / NCLT / RBI remaining uncomplied?

---

### Clause (vi) — Cost Records (Section 148)

**Required information:**
- Is the company required to maintain cost records u/s 148?
- If yes: Have such accounts and records been made and maintained?

---

### Clause (vii) — Statutory Dues

**(a) Regular Deposit of Statutory Dues:**
- PF, ESI, income tax, GST, customs duty, excise duty, cess, other statutory dues
- Are there arrears as at last date of FY outstanding for more than 6 months?

**(b) Dues not deposited on account of disputes:**
- Any amount not deposited on account of dispute pending before appellate authority?
- Forum, amount, period to which it relates?

---

### Clause (viii) — Unrecorded Income / Transactions Surrendered Under Any Scheme

- Any transactions not recorded in books surrendered during the year?
- Any corresponding tax on such income — paid or adjusted?

---

### Clause (ix) — Default in Loans / Borrowings

**(a)** Any default in repayment of loans/borrowings or payment of interest to financial institutions/banks/government/debenture holders?
**(b)** Any loan raised or pledge of securities done for a purpose other than that for which it was raised?
**(c)** Short-term funds used for long-term investments or vice versa?
**(d)** Any capital raised during the year — end use as stated in offer document?

---

### Clause (x) — IPO / FPO / Rights Issue / Preferential Allotment

**(a)** Public offer of securities (IPO/FPO)?
**(b)** Preferential allotment / private placement?
**(c)** End use of funds as per stated objectives?

---

### Clause (xi) — Frauds

**(a)** Any fraud by or on the company during the year?
**(b)** Whistle-blower complaints received?
**(c)** Report u/s 143(12) filed with Central Government (if applicable)?

---

### Clause (xii) — Nidhi Companies

Applicable only to Nidhi companies — net owned funds, deposits, ratio compliance.

---

### Clause (xiii) — Related Party Transactions

- All related party transactions in compliance with Section 177 (Audit Committee) and Section 188?
- Disclosed in financial statements as per Ind AS / AS?

---

### Clause (xiv) — Internal Audit

**(a)** Internal audit system commensurate with size and nature of business?
**(b)** Reports of internal auditors considered? (For companies required to have internal auditor)

---

### Clause (xv) — Non-Cash Transactions with Directors

- No non-cash transactions with directors or persons connected with them u/s 192?
- If yes: Approval obtained?

---

### Clause (xvi) — RBI Registration (NBFCs / HFCs)

- Company required to register u/s 45-IA of RBI Act?
- If yes: Valid CoR obtained?
- Nature of NBFC activity — reporting of systemic risk?

---

### Clause (xvii) — Cash Loss

- Company incurred cash loss in current FY?
- Cash loss in immediately preceding FY?

---

### Clause (xviii) — Resignation of Statutory Auditor

- Has the statutory auditor resigned during the year?
- Issues, objections, concerns raised in resignation letter addressed?

---

### Clause (xix) — Going Concern

- On the basis of financial ratios, ageing of receivables, net worth, etc. — any material uncertainty about company's ability to continue as a going concern?

---

### Clause (xx) — CSR Expenditure (Section 135)

**(a)** Amount to be spent per Section 135 for the year?
**(b)** Unspent CSR amount if any — transferred to specified fund?
**(c)** Administrative overheads — within prescribed limits?

---

### Clause (xxi) — Qualified / Adverse Remarks in Subsidiary / Associate Auditor's Report

- Consolidated financial statements include subsidiaries / associates / JVs?
- Were there any qualified or adverse remarks in any such entity's audit report?

---

## CARO Reporting Summary

After filling all clauses, generate:

```
CARO 2020 SUMMARY — [Company] | FY: [FY] | Auditor: [Firm]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total clauses: 21
Favourable remarks: [N]
Adverse / Unfavourable remarks: [N]
Not Applicable: [N]

Adverse remarks (summary):
  Clause (vii) — GST dues outstanding for >6 months: Rs.XX,XXX [disputed / undisputed]
  Clause (ix) — Default in loan repayment to [bank]: Rs.XX,XXX — [period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
