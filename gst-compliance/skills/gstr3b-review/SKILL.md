---
name: gstr3b-review
description: >
  Review GSTR-3B before filing. Checks ITC eligibility, identifies blocked credits (Section
  17(5)), calculates Rule 42/43 reversals, validates cash vs credit utilisation, computes
  interest on late payment, and ensures GSTR-2B reconciliation is complete. Critical for
  avoiding ITC mismatch notices.
when_to_use: >
  When the user wants to review GSTR-3B data, check ITC eligibility, calculate ITC
  reversals, determine cash balance requirement, or prepare the monthly tax computation.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# GSTR-3B Review

**FINANCIAL INTEGRITY**: GSTR-3B review and computation only. Do NOT submit until the HITL approval step is triggered, which will show the full checklist to the signing CA. All tax payments from the Electronic Cash Ledger require separate confirmation.

## Firm Context
!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null || echo "Run /cold-start:onboard-firm to set up firm profile"`

## Step 1 — Client, Period, and GSTIN

Collect:
- Client name and GSTIN
- Return period (month-year)
- Is this a QRMP filer? (file every quarter, PMT-06 monthly)

## Step 2 — Section 3.1 — Outward Supplies

| Head | Amount |
|---|---|
| 3.1(a) Taxable Outward Supplies (other than zero-rated) | |
| 3.1(b) Zero-Rated Outward Supplies (with IGST / LUT) | |
| 3.1(c) Nil-Rated / Exempt / Non-GST | |
| 3.1(d) Inward Supplies Taxable under Reverse Charge | |
| 3.1(e) Non-GST Supplies | |

Cross-check with GSTR-1 totals. Flag if difference > Rs.100 (rounding is common but should match).

## Step 3 — Section 4 — ITC Eligibility Analysis

**Critical: ITC can only be availed on eligible purchases.**

### 4A — ITC Available (from GSTR-2B)
Pull GSTR-2B summary: total ITC available as per auto-drafted portal data.

### Section 17(5) Blocked Credits — CHECK EACH CATEGORY
ITC is BLOCKED (cannot be claimed) on:
- [ ] Motor vehicles and conveyances (unless used for taxi, transport business, or resale)
- [ ] Food and beverages, outdoor catering
- [ ] Beauty treatment, health services, cosmetic surgery
- [ ] Club memberships
- [ ] Insurance of motor vehicles (unless registered for transport service)
- [ ] Rent-a-cab (unless providing taxable cab services)
- [ ] Construction / civil works (for immovable property)
- [ ] Works contract for immovable property (unless input service for same)
- [ ] Goods / services for personal consumption
- [ ] Goods lost / stolen / destroyed / written off / gift/sample above Rs.50K

Ask the user: "Are any of your purchases in these blocked categories? If yes, list them."

### Rule 42 — ITC Reversal on Mixed Use (Partly Business + Partly Exempt)
If the taxpayer makes both taxable and exempt supplies:
```
D1 = (Total ITC × Exempt Turnover) ÷ Total Turnover
D2 = ITC on Capital Goods × Exempt Turnover ÷ Total Turnover
Net ITC after reversal = Total ITC - D1 - D2
```

Ask: "Do you have any exempt supplies (e.g. land sale, exempt services)? If yes, provide turnover split."

### Rule 43 — ITC Reversal on Capital Goods Used for Exempt Supply
For capital goods used in both taxable and exempt supply: 5% per annum reversal.

### 4B — ITC Reversed During the Period
- Under Rule 42/43 (calculated above)
- TRAN-1/TRAN-2 credit reversal (if applicable)
- Any other reversals (credit note received, goods returned, etc.)

## Step 4 — Section 5 — Values of Exempt / Nil / Non-GST Supplies

This is informational — does not affect tax liability but must be complete.

## Step 5 — Tax Computation

Build the GSTR-3B tax liability table:

```
TAX LIABILITY COMPUTATION — [Client] | [GSTIN] | [Period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          | CGST     | SGST     | IGST     | CESS
─────────────────────────────────────────────────────────────────
OUTPUT TAX LIABILITY      |          |          |          |
3.1(a) Regular Supplies   | Rs.X     | Rs.X     | Rs.X     | Rs.X
3.1(d) RCM Inward Sup.   | Rs.X     | Rs.X     | Rs.X     |
TOTAL OUTPUT TAX          | Rs.X     | Rs.X     | Rs.X     | Rs.X
─────────────────────────────────────────────────────────────────
ITC AVAILABLE             |          |          |          |
From GSTR-2B              | Rs.X     | Rs.X     | Rs.X     | Rs.X
Less: Blocked Credits     |(Rs.X)    |(Rs.X)    |(Rs.X)    |
Less: Rule 42/43 Reversal |(Rs.X)    |(Rs.X)    |(Rs.X)    |
NET ITC                   | Rs.X     | Rs.X     | Rs.X     | Rs.X
─────────────────────────────────────────────────────────────────
SET OFF ORDER (Rule 88A)  |          |          |          |
IGST pays IGST first, then CGST, then SGST
CGST can set off CGST and IGST (in order)
SGST can set off SGST and IGST (in order)
─────────────────────────────────────────────────────────────────
TAX PAYABLE IN CASH       |          |          |          |
CGST Cash Payable         | Rs.X     |          |          |
SGST Cash Payable         |          | Rs.X     |          |
IGST Cash Payable         |          |          | Rs.X     |
Cess Cash Payable         |          |          |          | Rs.X
─────────────────────────────────────────────────────────────────
TOTAL CASH REQUIRED       | Rs.X,XX,XXX
```

## Step 6 — Interest on Late Payment

If filing after the due date OR if tax was payable last month but not paid:

```
Interest Calculation (Section 50):
Tax due: Rs.X  |  Due date: [date]  |  Payment date: [date]
Days delayed: N days
Interest = Rs.X × 18% × N ÷ 365 = Rs.Y (minimum Rs.1)
```

## Step 7 — Electronic Cash Ledger Check

Ask: "What is your current cash balance in the Electronic Cash Ledger?"
- CGST balance: Rs.X
- SGST balance: Rs.X
- IGST balance: Rs.X

If balance < cash required:
```
⚠ CASH LEDGER SHORTFALL:
CGST needed: Rs.X | Available: Rs.X | SHORTFALL: Rs.X
Action: Make payment via Challan PMT-06 before filing
Bank: Any authorised bank | Mode: NEFT/RTGS/Net Banking
```

## Step 8 — Final Checklist Before Approval

```
GSTR-3B PRE-FILING CHECKLIST — [Client] | [Period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] GSTR-1 filed and matches outward tax in 3.1
[ ] GSTR-2B reviewed — ITC figures reconciled
[ ] Blocked credits identified and removed
[ ] Rule 42/43 reversal calculated (if applicable)
[ ] Cash ledger has sufficient balance
[ ] Interest computed (if late filing)
[ ] Nil supply figures correct
[ ] Previous month's liability differences addressed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tax payable: Rs.X | Cash needed: Rs.X

When ready to file, say "Proceed with GSTR-3B filing for [GSTIN] [period]"
→ The HITL checklist will then appear for partner sign-off
```
