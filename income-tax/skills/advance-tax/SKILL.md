---
name: advance-tax
description: >
  Calculate quarterly advance tax instalments for individuals and businesses.
  Computes estimated annual income, tax liability, and required advance tax amounts
  for each instalment due date (15 June, 15 Sept, 15 Dec, 15 Mar). Also calculates
  interest u/s 234B and 234C for shortfalls.
when_to_use: >
  When the user wants to compute advance tax for a client, check if advance tax has
  been paid correctly, calculate shortfall interest, or plan advance tax payments.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Advance Tax Calculation

**FINANCIAL INTEGRITY**: Advance tax computation is an estimate. Always ask the CA to confirm before advising the client on payment amounts. Underpayment attracts interest; overpayment means cash flow loss.

## Applicability

Advance tax is payable by:
- Individuals with tax liability > Rs.10,000 after TDS credit
- All businesses and firms
- **Seniors (60+) are exempt** from advance tax if no business income

**Presumptive income taxpayers (44AD/ADA)**: Pay entire advance tax by 15 March (no quarterly instalment).

## Advance Tax Instalments (Section 211)

| Due Date | Minimum Cumulative % of Total Tax |
|---|---|
| 15 June | 15% |
| 15 September | 45% |
| 15 December | 75% |
| 15 March | 100% |

## Step 1 — Estimate Annual Income

Based on client's current year income (actual + projected):

| Source | Current Period (Actual) | Projected Full Year |
|---|---|---|
| Salary / Business Profit | Rs.X | Rs.X |
| Capital Gains (actual, if known) | Rs.X | Rs.X |
| Interest Income | Rs.X | Rs.X |
| Rental Income | Rs.X | Rs.X |
| Other Sources | Rs.X | Rs.X |
| **TOTAL INCOME** | Rs.X | Rs.X |
| Less: Chapter VI-A Deductions | (Rs.X) | (Rs.X) |
| **TAXABLE INCOME (estimated)** | | Rs.X |

## Step 2 — Compute Total Tax Liability

Apply slab rates (New Regime / Old Regime — as applicable):

**New Regime Slabs (AY 2025-26 onwards, default):**
- Up to Rs.3,00,000: Nil
- Rs.3,00,001 to Rs.7,00,000: 5%
- Rs.7,00,001 to Rs.10,00,000: 10%
- Rs.10,00,001 to Rs.12,00,000: 15%
- Rs.12,00,001 to Rs.15,00,000: 20%
- Above Rs.15,00,000: 30%
- Rebate u/s 87A: Tax = Nil if total income ≤ Rs.7,00,000

**Old Regime Slabs (if opted):**
- Up to Rs.2,50,000: Nil
- Rs.2,50,001 to Rs.5,00,000: 5%
- Rs.5,00,001 to Rs.10,00,000: 20%
- Above Rs.10,00,000: 30%
- Rebate u/s 87A: Tax = Nil if total income ≤ Rs.5,00,000

Add: Surcharge (if applicable) + 4% Health & Education Cess.

```
ADVANCE TAX COMPUTATION — [Client] | PAN: [PAN] | AY: [AY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated Annual Taxable Income   : Rs.X,XX,XXX
Tax on estimated income           : Rs.XX,XXX
Add: Surcharge                    : Rs.X,XXX
Add: Cess @ 4%                    : Rs.X,XXX
GROSS TAX LIABILITY               : Rs.XX,XXX
Less: TDS (from employer, bank)   : (Rs.XX,XXX)
NET TAX FOR ADVANCE TAX           : Rs.XX,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 3 — Instalment Schedule

```
ADVANCE TAX PAYMENT SCHEDULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instalment | Due Date   | Cumulative % | Amount Due | Already Paid | Balance
1st        | 15-Jun-[Y] | 15%          | Rs.X,XXX   | Rs.X,XXX     | Rs.X,XXX
2nd        | 15-Sep-[Y] | 45%          | Rs.X,XXX   | Rs.X,XXX     | Rs.X,XXX
3rd        | 15-Dec-[Y] | 75%          | Rs.X,XXX   | Rs.X,XXX     | Rs.X,XXX
4th        | 15-Mar-[Y] | 100%         | Rs.X,XXX   | Rs.X,XXX     | Rs.X,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 4 — Interest on Shortfall

**Interest u/s 234B** (failure to pay 90% of tax before end of year):
```
Tax payable > TDS: Rs.X | 90% threshold: Rs.X | Advance tax paid: Rs.X
If advance tax < 90%: Interest = shortfall × 1% per month
from 1 April (AY) to date of self-assessment tax payment
```

**Interest u/s 234C** (shortfall in instalment amounts):
For each instalment where cumulative payment < required %:
```
Instalment 1 (15 Jun): Required 15% = Rs.X | Paid Rs.X | Shortfall Rs.X
Interest = Shortfall × 1% × 3 months = Rs.X

Instalment 2 (15 Sep): Required 45% - paid so far | Interest for 3 months
Instalment 3 (15 Dec): Required 75% - paid so far | Interest for 3 months
Instalment 4 (15 Mar): No interest if full payment by 15 Mar
```

**Exception**: 234C interest NOT applicable if:
- Capital gains / casual income arises after the due date of instalment
- For companies: if they paid at least as much tax as was due (per tax return estimates)

## Step 5 — Payment Instructions

Advance tax is paid via:
- Challan 280 (Income Tax) → Type of Payment: 100 (Advance Tax)
- Online: https://eportal.incometax.gov.in → e-Pay Tax
- Bank: Authorised bank branches with Challan 280

```
PAYMENT ADVICE:
Next instalment: [Rs.X] due by [date]
PAN: [PANXXXXXXXX]
Assessment Year: [AY XXXX-XX]
Challan Type: 280 | Payment Code: 100 (Advance Tax)
```
