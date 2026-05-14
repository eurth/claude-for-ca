---
name: default-check
description: >
  Detect TDS defaults: late deduction, short deduction, non-deduction. Calculate interest
  u/s 201(1A). Check section-wise threshold breaches (194C, 194J, 192, etc.) and identify
  PAN-not-furnished cases requiring 20% TDS. Review challan dates vs deduction dates.
when_to_use: >
  When the user wants to check if TDS was deducted correctly and on time, identify
  TDS defaults before filing returns, or calculate interest for late payment.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# TDS Default Detection

**FINANCIAL INTEGRITY**: TDS defaults are serious — interest u/s 201(1A) applies from date payment was made (or credited) to actual deposit date. Non-compliance can lead to disallowance of expense u/s 40(a)(ia) and prosecution. Review findings before informing client.

## TDS Section Quick Reference

| Section | Nature of Payment | Rate | Threshold |
|---|---|---|---|
| 192 | Salary | Slab rate | Above basic exemption |
| 193 | Interest on Securities | 10% | Rs.10,000 |
| 194 | Dividend | 10% | Rs.5,000 |
| 194A | Interest (bank/other) | 10% | Rs.40,000 (bank), Rs.5,000 (other) |
| 194B | Winnings — lottery/crossword | 30% | Rs.10,000 per transaction |
| 194C | Contractor / Subcontractor | 1% (individual/HUF) / 2% (others) | Rs.30,000 per payment / Rs.1,00,000 p.a. |
| 194D | Insurance commission | 5% | Rs.15,000 |
| 194H | Commission / Brokerage | 5% | Rs.15,000 |
| 194I | Rent (land/building/furniture) | 10% | Rs.2,40,000 p.a. |
| 194IA | Transfer of immovable property | 1% | Rs.50,00,000 |
| 194IB | Rent by individual/HUF | 5% | Rs.50,000 per month |
| 194J | Professional fees/Technical | 10% (professional) / 2% (technical/call centre) | Rs.30,000 |
| 194K | Income from MF units | 10% | Rs.5,000 |
| 194M | Contractor/Commission by individual/HUF | 5% | Rs.50,00,000 p.a. |
| 194N | Cash withdrawal | 2% (if no ITR last 3 yrs: 5%) | Rs.1 Cr (normal), Rs.20L (non-filer) |
| 194O | TDS by e-commerce operator | 1% | — |
| 194Q | Purchase of goods | 0.1% | Rs.50L from single seller |
| 195 | Payment to non-residents | As per DTAA or rates | All amounts |

## Step 1 — Collect Payment Ledger

Ask the user to provide (or pull from Tally):
- All payments/credits subject to TDS for the quarter
- Date of payment/credit (whichever is earlier = date of deduction)
- TDS deducted amount and date
- Challan date (date of payment to government)
- PAN of deductee

## Step 2 — Default Analysis

For each transaction:
```
TRANSACTION ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Party       | Date of Pmt | Amount   | Section | Rate | TDS Due | TDS Deducted | Challan Date | Default?
────────────────────────────────────────────────────────────────────────────────────────────────────
ABC Pvt Ltd | 15-Apr-2026 | 1,00,000 | 194C    | 2%   | 2,000   | 2,000        | 07-May-2026  | ✓ OK
XYZ Traders | 20-Apr-2026 | 50,000   | 194C    | 2%   | 1,000   | 0            | N/A          | ⚠ NON-DEDUCTION
DEF Corp    | 01-Apr-2026 | 80,000   | 194J    | 10%  | 8,000   | 6,000        | 07-May-2026  | ⚠ SHORT DEDUCTION
GHI Ltd     | 10-Apr-2026 | 2,00,000 | 194C    | 2%   | 4,000   | 4,000        | 15-Jun-2026  | ⚠ LATE DEPOSIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 3 — PAN Not Furnished Cases

If PAN not available for a deductee: TDS rate is HIGHER of:
- The rate in force under the section, OR
- 20%

Flag each such case and calculate excess TDS that should have been deducted.

## Step 4 — Interest Calculation (Section 201(1A))

**Late deduction**: 1% per month from date of deduction to actual deduction date
**Late deposit**: 1.5% per month from date of deduction to actual deposit date

```
INTEREST CALCULATION (Section 201(1A)):
Party: XYZ Traders | Non-deduction from 20-Apr-2026 to 07-May-2026 (18 days = 1 month)
TDS Amount: Rs.1,000 | Interest @ 1% × 1 month = Rs.10

Party: GHI Ltd | Late deposit from 10-Apr-2026 to 15-Jun-2026 (66 days = 3 months)
TDS Amount: Rs.4,000 | Interest @ 1.5% × 3 months = Rs.180
```

## Step 5 — Section 40(a)(ia) Disallowance

If TDS not deducted (or deducted but not paid to government by due date — last of Feb for March, 7th of next month for others):
30% of the expense is disallowed u/s 40(a)(ia).

Flag which expenses are at risk.

## Step 6 — Summary and Remediation

```
TDS DEFAULT SUMMARY — [Client] | TAN: [TAN] | Quarter: [Q] FY: [FY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total defaults found: [N]
  Non-deduction: [N] cases | TDS shortfall: Rs.X
  Short deduction: [N] cases | Shortfall: Rs.X  
  Late deposit: [N] cases | TDS involved: Rs.X

Interest payable u/s 201(1A): Rs.X
Sec 40(a)(ia) disallowance risk: Rs.X (30% of Rs.X expenditure)

REMEDIATION STEPS:
1. Deduct TDS from next payment / recover from party for non-deduction cases
2. Pay shortfall TDS via Challan 281 (TDS) immediately
3. Deposit interest separately in Challan 281
4. File correction TDS return (24Q/26Q) after payment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
