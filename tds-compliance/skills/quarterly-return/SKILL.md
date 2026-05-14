---
name: quarterly-return
description: >
  Review and assist with TDS quarterly return filing (24Q for salary, 26Q for non-salary,
  27Q for NRI payments, 27EQ for TCS). Checks challan-to-deductee mapping, PAN validation,
  late fee calculation (Section 234E), and interest on late deposit. Covers RPU (Return
  Preparation Utility) data format.
when_to_use: >
  When the user wants to prepare or review a TDS quarterly return (24Q/26Q/27Q/27EQ),
  file it, or check for errors before submission.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# TDS Quarterly Return — 24Q / 26Q / 27Q

**FINANCIAL INTEGRITY**: TDS returns are due by 31 July (Q1), 31 Oct (Q2), 31 Jan (Q3), 31 May (Q4). Late filing attracts Rs.200/day late fee u/s 234E — minimum Rs.200/day, maximum total TDS amount. Ensure all challans are matched before filing.

## Return Forms Reference

| Form | Quarter | Nature |
|---|---|---|
| 24Q | Q1-Q4 | TDS on Salary (Section 192) |
| 26Q | Q1-Q4 | TDS on other than salary — domestic |
| 27Q | Q1-Q4 | TDS on payments to non-residents |
| 27EQ | Q1-Q4 | TCS (Tax Collected at Source) |

## Due Dates

| Quarter | Period | Due Date |
|---|---|---|
| Q1 | April – June | 31 July |
| Q2 | July – September | 31 October |
| Q3 | October – December | 31 January |
| Q4 | January – March | 31 May |

## Step 1 — Prepare Input Data

Collect from client:
1. **Deductor details**: TAN, company name, PAN, address, type of deductor (govt/non-govt)
2. **Challan list**: For each challan deposited — BSR code, date, serial no., amount, section
3. **Deductee list**: Name, PAN, amount paid, TDS deducted, section, type

## Step 2 — Challan Verification

Before mapping challans to deductees:
- [ ] Verify BSR code format (7 digits)
- [ ] Verify challan serial number from bank counterfoil
- [ ] Challan date must be within the quarter (or before 31 May for Q4)
- [ ] Amount in challan >= total TDS mapped to it
- [ ] Any excess in challan must be tagged as "surplus" or used in next quarter

```
CHALLAN VERIFICATION:
BSR Code | Date        | Challan No. | Amount   | Section | Status
1234567  | 07-May-2026 | 00234       | Rs.2,000 | 194C    | ✓ Verified
7654321  | 07-Aug-2026 | 00456       | Rs.5,000 | 194J    | ✓ Verified
```

## Step 3 — PAN Validation

For each deductee:
- [ ] PAN format: 5 letters + 4 digits + 1 letter (e.g. ABCDE1234F)
- [ ] 4th character: P = Individual, C = Company, H = HUF, F = Firm, B = BOI, A = AOP
- [ ] 5th character = first letter of last name (individual) or entity name
- [ ] If PAN not available: use "PANNOTAVBL" for existing deductees with PAN, or "PANAPPLIED" for new

Flag: Any invalid PAN format — will cause return rejection.

## Step 4 — Late Fee Calculation (Section 234E)

```
LATE FEE CALCULATION:
Quarter Q[N] | Due date: [date] | Filing date: [date]
Days delayed: [N] days
Late fee = Rs.200 × [N] days = Rs.X (maximum = Total TDS in the return)
```

Note: Late fee is a separate line item in the return — must be paid before filing.

## Step 5 — Interest on Late Deposit

Already covered in default-check skill. Ensure interest is paid and reflected in return.

## Step 6 — Return File Generation

The TDS return is filed using:
- NSDL Return Preparation Utility (RPU) — downloadable from NSDL/TIN website
- File validation using FVU (File Validation Utility)
- Submit at TIN facilitation centre or online via TRACES

Key files generated:
- `24Q_[TAN]_Q[N]_FY[XXXX].fvu` — validated file for submission

## Step 7 — Pre-Filing Checklist

```
24Q / 26Q PRE-FILING CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] All challans verified — BSR code, date, amount
[ ] Total TDS in challans >= Total TDS in deductee list
[ ] No duplicate PAN entries
[ ] No invalid PAN format
[ ] Interest/late fee paid (if applicable)
[ ] FVU validation passed (no errors)
[ ] For 24Q Q4: Salary TDS computa for each employee complete
[ ] Authorised signatory DSC ready
[ ] TAN registered on TRACES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
After filing:
[ ] Provisional receipt from TIN (with token number)
[ ] Update TRACES login for Form 16/16A availability
[ ] Inform deductees that Form 16/16A will be available in [N] weeks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

When ready to file, say "File TDS return for [TAN] [Form] Q[N]" — the HITL guardrail will show the verification checklist.
