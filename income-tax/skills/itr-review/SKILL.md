---
name: itr-review
description: >
  Review Income Tax Return (ITR) computation before filing. Cross-checks ITR data against
  Form 26AS, AIS (Annual Information Statement), and TIS. Verifies deductions (80C/80D/
  80G/80GG/others), capital gains schedule, house property income, and identifies discrepancies.
  Covers all ITR forms: ITR-1 to ITR-7.
when_to_use: >
  When the user wants to review an ITR computation, check against 26AS/AIS, verify
  deductions, review capital gains, or prepare the income tax computation for a client.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# ITR Review — Pre-Filing Verification

**FINANCIAL INTEGRITY**: An incorrect ITR can attract notices, penalties under Section 270A, and prosecution in fraud cases. This review does NOT replace the CA's professional judgment. All ITRs must be e-verified by the assessee (OTP/EVC/DSC) and the CA's digital signature must be valid if certification is required.

## Firm Context
!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null || echo "Run /cold-start:onboard-firm to set up firm profile"`

## Step 1 — Client Information

Collect:
- Client name, PAN, date of birth / incorporation
- Assessment Year (e.g. 2026-27)
- Residential status (Resident Ordinary / Resident Not Ordinary / Non-Resident)
- ITR form to be filed (ITR-1 / 2 / 3 / 4 / 5 / 6 / 7)
- Sources of income

**ITR Form Selection Guide:**
| Scenario | ITR Form |
|---|---|
| Salaried individual, interest income < Rs.50L, no capital gains | ITR-1 (Sahaj) |
| Individual/HUF with capital gains or foreign assets | ITR-2 |
| Individual/HUF with business/profession income | ITR-3 |
| Individual/HUF/Firm under presumptive scheme (44AD/44ADA) | ITR-4 (Sugam) |
| Firms, LLPs, AOP, BOI | ITR-5 |
| Companies | ITR-6 |
| Trusts, political parties, research associations (12A/10(23C)) | ITR-7 |

## Step 2 — Form 26AS and AIS Cross-Check

**Critical**: ITR figures must be consistent with Form 26AS and AIS.

### From Form 26AS, verify:
- [ ] All TDS deducted by employers/banks/others matches "Tax Deducted at Source" in ITR
- [ ] Advance tax payments match
- [ ] Self-assessment tax paid matches
- [ ] TCS collected (if applicable)
- [ ] Any SFT (Specified Financial Transaction) entries

### From AIS (Annual Information Statement), check:
- [ ] Salary reported matches Part B / Form 16
- [ ] Dividend income matches
- [ ] Interest income from bank accounts matches
- [ ] Capital gains transactions from broker/mutual fund
- [ ] Rent received matches TDS certificates
- [ ] Any high-value transactions that should be declared

Mismatch flagging:
```
26AS / AIS MISMATCH REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Head           | As per 26AS/AIS | As per ITR Draft | Difference
Salary (TDS)   | Rs.X            | Rs.X             | Rs.X ⚠
Bank Interest  | Rs.X            | Rs.X             | OK ✓
Dividend       | Rs.X            | Rs.X             | Rs.X ⚠
Capital Gains  | Rs.X            | Rs.X             | OK ✓
```

## Step 3 — Income Computation Review

### Salary Income (Section 15-17)
- [ ] Gross salary matches Form 16 Part A
- [ ] Standard deduction Rs.50,000 applied (for AY 2025-26 and earlier) or Rs.75,000 (new regime from AY 2024-25)
- [ ] HRA exemption u/s 10(13A): min of [actual HRA / rent paid - 10% salary / 40% or 50% salary]
- [ ] Professional tax deduction
- [ ] Any other allowances (LTA, medical — check exemption limits)
- [ ] Employer's PF contribution > Rs.7.5L taxable

### House Property Income (Section 22-27)
- [ ] Rental income declared (if rented out)
- [ ] Standard deduction 30% applied
- [ ] Municipal taxes paid deducted
- [ ] Interest on home loan: Rs.2L limit for self-occupied
- [ ] Pre-construction interest: 1/5th for 5 years (after construction)

### Capital Gains
Use the separate `/income-tax:capital-gains` skill for detailed computation.
Quick checks:
- [ ] STCG on listed equity: 20% (post FY 2024-25 amendment) / old rate 15%
- [ ] LTCG on listed equity: 10% above Rs.1.25L (post FY 2024-25) / old Rs.1L
- [ ] LTCG on property: 12.5% without indexation (post FY 2024-25) / old 20% with indexation
- [ ] STCG on debt mutual funds: slab rates (post 1 Apr 2023)

### Business/Profession Income
- [ ] Books of accounts maintained (if turnover > Rs.1 Cr for business / Rs.50L for profession)
- [ ] Tax audit required? (Sec 44AB) — If yes, 3CA/3CB + 3CD mandatory
- [ ] Presumptive: 8% / 6% (44AD) — digital receipts qualify for 6%
- [ ] Disallowances under Section 40/40A (cash payments > Rs.10,000, related-party excessive payments)
- [ ] Depreciation schedule correct (WDV / straight-line)

## Step 4 — Deductions (Chapter VI-A)

| Section | Deduction | Limit | Check |
|---|---|---|---|
| 80C | LIC premium, PPF, ELSS, school fees, home loan principal | Rs.1,50,000 | |
| 80CCC | Pension fund contribution | Rs.1,50,000 (within 80C limit) | |
| 80CCD(1) | Employee NPS contribution | Rs.1,50,000 (within 80C) | |
| 80CCD(1B) | Additional NPS contribution | Rs.50,000 | |
| 80D | Medical insurance premium | Rs.25,000 (self) / Rs.50,000 (senior citizen parent) | |
| 80DD | Disabled dependent | Rs.75,000 / Rs.1,25,000 | |
| 80E | Education loan interest | No limit (first 8 years) | |
| 80G | Donations | 50% or 100% of amount (check NGO approval) | |
| 80GG | Rent paid (no HRA) | Least of: Rs.5,000/month / 25% of income / actual rent - 10% | |
| 80TTA | Savings bank interest | Rs.10,000 | |
| 80TTB | Interest (senior citizens 60+) | Rs.50,000 | |

**Old Regime vs New Regime** (from AY 2024-25, new regime is default):

New Regime: No deductions under Chapter VI-A (except 80CCD(2) employer NPS), but lower slab rates.
Old Regime: All deductions available.

Compute tax under both regimes and recommend.

## Step 5 — Tax Computation and TDS Credit

```
TAX COMPUTATION — [Client] | PAN: [PAN] | AY: [AY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INCOME:
Salary / Business Income   : Rs.X,XX,XXX
House Property Income      : Rs.XX,XXX
Capital Gains (STCG/LTCG)  : Rs.XX,XXX
Other Sources (Interest etc): Rs.XX,XXX
GROSS TOTAL INCOME         : Rs.X,XX,XXX
Less: Chapter VI-A Deductions: (Rs.XX,XXX)
TOTAL TAXABLE INCOME       : Rs.X,XX,XXX

TAX CALCULATION (Old Regime / New Regime — whichever selected):
Basic Tax                  : Rs.XX,XXX
Surcharge (if applicable)  : Rs.X,XXX
Health & Education Cess 4% : Rs.X,XXX
TOTAL TAX LIABILITY        : Rs.XX,XXX

TDS CREDITS:
TDS from employer (24Q)    : Rs.XX,XXX
TDS from bank (26Q)        : Rs.X,XXX
Advance tax paid           : Rs.X,XXX
TOTAL CREDITS              : Rs.XX,XXX

BALANCE PAYABLE / REFUND   : Rs.X (Pay / Refund)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 6 — Self-Assessment Tax and Interest

If tax payable after TDS credit:
- Pay as Self-Assessment Tax via Challan 280 before filing ITR
- Interest u/s 234B: 1% per month on unpaid tax if > 10% of total tax
- Interest u/s 234C: 1% per month on shortfall in advance tax instalments

## Step 7 — Final Pre-Filing Checklist

```
ITR PRE-FILING CHECKLIST — [Client] | [AY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] PAN active (not operative / inoperative)
[ ] Aadhaar linked to PAN (mandatory)
[ ] Bank account pre-validated for refund
[ ] 26AS/AIS reviewed — all income declared
[ ] All TDS credits matched
[ ] Self-assessment tax paid (if applicable) — Challan in 26AS
[ ] ITR form correct for the sources of income
[ ] Digital signature / EVC ready for e-verification
[ ] Original ITR due date: 31 July (non-audit) / 31 Oct (audit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
