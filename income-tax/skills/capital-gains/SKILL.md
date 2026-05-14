---
name: capital-gains
description: >
  Compute Short-Term and Long-Term Capital Gains for equity shares, equity mutual funds,
  debt mutual funds, property (land/building), bonds, and other assets. Applies correct
  holding periods, tax rates, indexation (for applicable assets), set-off and carry-forward
  rules. Covers post-FY 2024-25 amendments to STCG/LTCG rates.
when_to_use: >
  When a client has sold shares, mutual funds, property, or any capital asset and
  needs the capital gains computation. Also for planning tax on proposed sales.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Write
  - Bash(python3 *)
---

# Capital Gains Computation

**FINANCIAL INTEGRITY**: Capital gains computation uses indexed cost of acquisition, grandfathering provisions, and asset-specific rules. An incorrect computation leads to under/over payment of tax. Review by the CA is mandatory before filing.

## Holding Period Reference

| Asset | STCG Period | LTCG Period | LTCG Indexation |
|---|---|---|---|
| Listed equity shares | ≤ 12 months | > 12 months | Not available |
| Equity-oriented MF | ≤ 12 months | > 12 months | Not available |
| Unlisted shares | ≤ 24 months | > 24 months | Available |
| Debt MF (units acquired before 1 Apr 2023) | ≤ 36 months | > 36 months | Available |
| Debt MF (units acquired on or after 1 Apr 2023) | All periods | N/A | N/A — slab rates always |
| Land / Building | ≤ 24 months | > 24 months | Available |
| Gold / Jewellery | ≤ 36 months | > 36 months | Available |
| Listed bonds/debentures | ≤ 12 months | > 12 months | Not available |

## Tax Rates (Post FY 2024-25 — Budget 2024 Amendments)

| Asset | STCG Rate | LTCG Rate | LTCG Exemption |
|---|---|---|---|
| Listed equity (Section 111A) | 20% | 12.5% | First Rs.1,25,000 exempt u/s 112A |
| Equity MF (equity-oriented) | 20% | 12.5% | First Rs.1,25,000 exempt u/s 112A |
| Unlisted shares | Slab rates | 12.5% (no indexation from FY 2024-25) | Nil |
| Property | Slab rates | 12.5% (no indexation) | Nil (can opt for old 20% with indexation for property held before 23 Jul 2024) |
| Gold / Debt (pre-Apr 2023) | Slab rates | 12.5% (no indexation) | Nil |
| Debt MF (post-Apr 2023) | Slab rates | Slab rates | — |

**Grandfathering (Section 112A / 55(2)(AC)):**
For listed equity/equity MF purchased before 31 Jan 2018:
- Cost of Acquisition = higher of (actual cost OR fair market value on 31 Jan 2018, capped at sale price)

## Step 1 — Collect Transaction Data

For each capital asset sold, collect:
- Asset name / description
- Date of acquisition + cost of acquisition
- Date of sale + sale consideration
- Any transfer expenses (brokerage, stamp duty, registration, etc.)
- For property: improvement costs + dates

## Step 2 — Determine Holding Period and Category

For each transaction, calculate:
- Holding period = Date of Sale - Date of Acquisition (in months)
- Classify as STCG or LTCG based on table above

## Step 3 — Compute Capital Gains

### For Equity / Listed Shares / Equity MF (LTCG with Grandfathering):
```
Sale Consideration                  : Rs.X
Less: Transfer Expenses             : (Rs.X)
Net Sale Consideration              : Rs.X
Less: Cost of Acquisition
  (Higher of actual cost or FMV
   on 31 Jan 2018, if pre-2018 purchase,
   capped at sale price)            : (Rs.X)
LTCG                                : Rs.X

Exemption u/s 112A: First Rs.1,25,000 of LTCG from all eligible assets
Tax on LTCG in excess of Rs.1,25,000: @ 12.5%
```

### For Property / Unlisted Shares (LTCG):
```
Sale Consideration (or Stamp Duty Value, whichever higher — Section 50C)
                                    : Rs.X
Less: Transfer Expenses             : (Rs.X)
Net Sale Consideration              : Rs.X
Less: Indexed Cost of Acquisition
  (CoA × CII of year of sale ÷ CII of year of acquisition)
  CII for FY 2025-26 = [348] (update from CBDT notification)
                                    : (Rs.X)
Less: Indexed Cost of Improvement   : (Rs.X)
LTCG                                : Rs.X
Tax @ 12.5% (no indexation from 23 Jul 2024)
OR Tax @ 20% with indexation (property held before 23 Jul 2024 — option available) : Rs.X
```

### Section 50C — Stamp Duty Value
If property sold below stamp duty value:
- Sale consideration = stamp duty value (for tax purposes)
- Exception: if difference is ≤ 10% of stamp duty value, actual consideration is used

### Exemptions Available (Sections 54 / 54F / 54EC):
| Section | Available For | Condition |
|---|---|---|
| 54 | Residential property LTCG | Invest in new residential property within 1/2 years (forward) or 3 years (construction) |
| 54B | Agriculture land LTCG | Reinvest in agricultural land within 2 years |
| 54EC | Any LTCG | Invest in NHAI/REC/PFC bonds within 6 months — max Rs.50L per year |
| 54F | Any LTCG (other than house) | Invest entire net sale in residential property — must not own >2 houses |

## Step 4 — Set-Off and Carry-Forward (Section 70-74)

Set-off rules:
- STCL can set off STCG or LTCG
- LTCL can only set off LTCG (cannot set off STCG)
- Losses from equity (Section 111A/112A) can only set off against same category

Carry-forward: Capital losses can be carried forward for 8 years (if ITR filed before due date).

```
SET-OFF COMPUTATION:
STCG this year     : Rs.X
STCL this year     : (Rs.X)
Brought fwd STCL   : (Rs.X) [from previous years]
NET STCG           : Rs.X

LTCG this year     : Rs.X
LTCL this year     : (Rs.X)
NET LTCG           : Rs.X

Taxable STCG @ 20% : Rs.X (tax Rs.X)
Taxable LTCG @ 12.5% (after Rs.1,25,000 exemption): Rs.X (tax Rs.X)

Losses to carry forward to next year:
  STCL c/f: Rs.X  |  LTCL c/f: Rs.X
```

## Step 5 — Capital Gains Summary for ITR

```
CAPITAL GAINS SCHEDULE — [Client] | PAN: [PAN] | AY: [AY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STCG (Section 111A — listed equity):
  Gross: Rs.X | Losses: Rs.X | NET: Rs.X | Tax @ 20%: Rs.X

LTCG (Section 112A — listed equity/equity MF):
  Gross: Rs.X | Exemption Rs.1,25,000: Rs.X | Taxable: Rs.X | Tax @ 12.5%: Rs.X

LTCG (Section 112 — other assets — property, unlisted):
  Gross: Rs.X | Tax @ 12.5%: Rs.X

STCG / LTCG Losses carried forward:
  STCL to carry forward: Rs.X | LTCL to carry forward: Rs.X
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
