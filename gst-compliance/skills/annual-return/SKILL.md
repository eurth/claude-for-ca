---
name: annual-return
description: >
  Assist with GSTR-9 (annual return) and GSTR-9C (reconciliation statement). Cross-checks
  annual GSTR-9 figures against GSTR-1/3B filed during the year, identifies differences,
  computes additional liability if any, and helps draft GSTR-9C reconciliation statement
  for audit turnover clients.
when_to_use: >
  During annual return season (Jan-Mar). When the user wants to prepare GSTR-9 for a
  client, reconcile annual figures, check GSTR-9C applicability, or identify differences
  between annual books and returns filed.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# GSTR-9 / GSTR-9C — Annual Return

**FINANCIAL INTEGRITY**: GSTR-9 is a declaration on oath. Any additional tax liability declared must be paid before filing. GSTR-9C is a certification by a CA/CMA — never certify without full reconciliation. Do NOT file until partner has reviewed and approved.

## Applicability

| Turnover | GSTR-9 | GSTR-9C |
|---|---|---|
| Up to Rs.2 Cr | Optional (waived by notification) | Not required |
| Rs.2 Cr to Rs.5 Cr | Mandatory | Not required |
| Above Rs.5 Cr | Mandatory | Mandatory (CA/CMA certification) |
| Composition dealers | GSTR-9A | Not applicable |

Exempt categories: ISD, casual taxable persons, NRTPs.

## Step 1 — Data Collection

Collect for the full financial year:
1. GSTR-1 filing summary (month-wise totals)
2. GSTR-3B filing summary (month-wise totals)
3. Annual books (P&L revenue, purchases from audited accounts or trial balance)
4. ITC ledger from Tally (input credit availed month-wise)

## Step 2 — GSTR-9 Table-by-Table Review

**Table 4 — Details of outward supplies (from GSTR-1)**
Pull sum of all 12 months GSTR-1:
- 4A: Supplies other than reverse charge (B2B + B2C)
- 4B: Outward supplies on which RCM applicable
- 4C: Zero-rated supplies (export + SEZ with IGST)
- 4D: Supplies to SEZ without payment
- 4E: Deemed exports
- 4F: Advances on which tax was paid

Compare with books (audited revenue).

**Table 5 — Outward supplies not included in GSTR-3B**
- Nil, exempt, non-GST supplies
- No-supply transactions

**Table 6 — ITC availed (from GSTR-3B sum)**
Break down by:
- 6A: Total ITC as per GSTR-3B
- 6B: ITC on inputs, capital goods, input services — break-up
- 6C: Inward supplies on RCM basis (registered)
- 6D: Inward on RCM basis (unregistered)
- 6E: ITC reclaimed after reversal in earlier periods

**Table 7 — ITC reversals**
Sum of Rule 42/43 reversals declared in monthly GSTR-3B.

**Table 8 — Reconciliation of ITC with GSTR-2A**
One of the most scrutinised tables:
- 8A: ITC as per GSTR-2A (annual auto-populated)
- 8B: ITC availed (from Table 6)
- 8C: ITC in GSTR-2A but NOT availed — carry forward for next year
- 8D: Difference (8A - 8B - 8C) — this is the "ITC lapse" that department notices

**Table 9 — Tax payable and paid**
For each tax period, reconcile:
- Tax payable as per GSTR-3B
- Tax actually paid via cash + credit
- Any differences → additional payment needed

**Table 10 — Additions/Amendments**
Any supplies that should have been declared in GSTR-1/GSTR-3B but were not.

**Table 11 — ITC reversals not already reversed**
Any ITC that should have been reversed but was not done in monthly returns.

## Step 3 — Reconciliation Statement (GSTR-9C — for turnover > Rs.5 Cr)

```
GSTR-9C RECONCILIATION — [Client] | FY [XXXX-XX]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART A — RECONCILIATION OF TURNOVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Turnover as per audited accounts         | Rs.X,XX,XXX
2. Unbilled revenue at end of year          | Rs.XX,XXX
3. Unadjusted advances at end of year       | Rs.XX,XXX
4. Credit notes issued after filing cutoff  | (Rs.XX,XXX)
5. Trade discounts not included in invoices | (Rs.XX,XXX)
6. Turnover as per GSTR-9 (Table 5N/10/11) | Rs.X,XX,XXX
─────────────────────────────────────────────────────────────
DIFFERENCE (1 to 5 vs 6)                    | Rs.X [EXPLAIN]

PART B — RECONCILIATION OF TAX PAID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tax payable on reconciled turnover          | Rs.X,XX,XXX
Tax actually paid (as per GSTR-9)           | Rs.X,XX,XXX
Unreconciled difference (if any)            | Rs.XX,XXX

PART C — RECONCILIATION OF ITC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITC as per audited accounts                 | Rs.X,XX,XXX
ITC availed as per GSTR-3B                  | Rs.X,XX,XXX
ITC not availed (lapsed / time-barred)      | Rs.XX,XXX
ITC reversed (Rule 42/43 / Section 17(5))   | Rs.XX,XXX
Net claimable ITC (books)                   | Rs.X,XX,XXX
Difference from GSTR-3B                     | Rs.X [EXPLAIN]
```

## Step 4 — Additional Liability + Payment

If GSTR-9 shows additional liability not paid during the year:
- Pay using DRC-03 (voluntary payment) before or at the time of filing GSTR-9
- Interest applies from due date of the return for the respective month to date of payment

## Step 5 — CA Certificate (GSTR-9C Part B)

Generate the certification language:
```
I/We [CA Name], [Membership No.], [Firm Name and Reg. No.] have examined the books of account
of [Client Name] (GSTIN: [GSTIN]) for the financial year [FY], and certify that the information
given in Parts I, II, III, IV and V of Form GSTR-9C is true and correct to the best of my/our
knowledge and based on the information and explanations given to me/us, and to the best of my/our
knowledge the information given therein are correct and complete.
```

Note: The CA must personally verify before signing — never use this certificate without review.
