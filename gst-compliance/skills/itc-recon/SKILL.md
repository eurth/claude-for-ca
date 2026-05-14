---
name: itc-reconcile
description: >
  Reconcile Input Tax Credit: compare GSTR-2B (auto-drafted) with the Purchase Register.
  Identify invoices present in one but not the other, excess ITC claims, invoices filed
  by vendor but not in books, blocked credits (Section 17(5)), and the time limit for
  ITC availing (Section 16(4) — ITC to be claimed by 30 Nov of next FY or before filing
  annual return, whichever is earlier).
when_to_use: >
  When the user wants to reconcile ITC, compare GSTR-2B with purchase register,
  find missing invoices, check ITC eligibility, or prepare ITC summary for GSTR-3B.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# ITC Reconciliation (GSTR-2B vs Purchase Register)

**FINANCIAL INTEGRITY**: ITC reconciliation informs how much credit can be claimed. Over-claiming ITC attracts interest at 24% + penalty. Under-claiming is a loss to the client. This reconciliation must be signed off by the CA before filing GSTR-3B.

## Firm Context
!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null || echo "Run /cold-start:onboard-firm to set up firm profile"`

## Step 1 — Gather Data

**GSTR-2B Data**: Ask the user to:
1. Go to GST portal → Services → Returns → GSTR-2B
2. Download the Excel file (or JSON) for the period
3. Share it here

**Purchase Register**: Accept from Tally or Master Accounts Excel. Columns needed:
- Vendor Name, Vendor GSTIN, Invoice Number, Invoice Date, Taxable Value, CGST, SGST, IGST, Total

## Step 2 — Reconciliation

Match invoices between GSTR-2B and Purchase Register on:
1. **Primary key**: Supplier GSTIN + Invoice Number
2. **Secondary check**: Invoice date + approximate amount (±5%)

Classify each entry:

| Category | Code | Action Required |
|---|---|---|
| Matched — amount same | ✓ OK | None — claim ITC |
| In GSTR-2B, NOT in purchase register | 2B-ONLY | Check with vendor — book the invoice |
| In purchase register, NOT in GSTR-2B | PR-ONLY | Vendor has not filed GSTR-1 — chase vendor |
| Matched — amount different | AMT-DIFF | Verify with original invoice — raise credit/debit note |
| Invoice date older than 2 years | TIME-BAR | ITC lapse — Section 16(4) |
| Blocked supply (Section 17(5)) | BLOCKED | Do NOT claim — mark as ineligible |

## Step 3 — Section 16 Timeline Check

ITC cannot be availed after:
- **Current year**: 30 November of the following year, or
- Before filing annual return (GSTR-9), whichever is earlier

Flag any invoices where the financial year of supply has already crossed the ITC deadline.

```
⚠ TIME-BARRED ITC WARNING:
These invoices are from FY [X] — ITC deadline has passed:
  Vendor: ABC Pvt Ltd | Invoice: ABC/001 | Date: 15-Mar-[old FY] | ITC: Rs.18,000 — LAPSED
  [Total lapsed ITC: Rs.XX,000]
Do NOT claim this ITC in GSTR-3B.
```

## Step 4 — Vendor Compliance Analysis

For vendors with invoices in Purchase Register but NOT in GSTR-2B:

| Vendor | Total Purchases | ITC at Risk | Last GSTR-1 Filed |
|---|---|---|---|
| XYZ Traders | Rs.5,40,000 | Rs.48,600 | [Check portal] |
| ABC Services | Rs.1,20,000 | Rs.21,600 | [Check portal] |

Draft a vendor follow-up email:
```
Subject: GSTR-1 Filing — Invoice Discrepancy for [Month]

Dear [Vendor Name],

We have observed that the following invoices issued by you have not been reflected
in our GSTR-2B for [Period]. This prevents us from claiming the applicable ITC.

Invoice No. | Date | Amount | ITC
[details]

Request you to file/correct your GSTR-1 at the earliest or provide confirmation
of the filing status. ITC can only be claimed once the data appears in our GSTR-2B.

Regards,
[CA Firm Name]
```

## Step 5 — ITC Summary

```
ITC RECONCILIATION SUMMARY — [Client] | [GSTIN] | [Period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                          | CGST     | SGST     | IGST     | TOTAL
─────────────────────────────────────────────────────────────────
A. GSTR-2B Total ITC      | Rs.X     | Rs.X     | Rs.X     | Rs.X
B. Purchase Register ITC  | Rs.X     | Rs.X     | Rs.X     | Rs.X
C. Matched (A∩B)          | Rs.X     | Rs.X     | Rs.X     | Rs.X
D. In 2B not in PR        | Rs.X     | Rs.X     | Rs.X     | Rs.X
E. In PR not in 2B        | Rs.X     | Rs.X     | Rs.X     | Rs.X
F. Amount mismatch        | Rs.X     | Rs.X     | Rs.X     | Rs.X
G. Blocked credits (17(5))| Rs.X     | Rs.X     | Rs.X     | Rs.X
H. Time-barred ITC        | Rs.X     | Rs.X     | Rs.X     | Rs.X
─────────────────────────────────────────────────────────────────
NET CLAIMABLE ITC (C-G-H) | Rs.X     | Rs.X     | Rs.X     | Rs.X
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vendors to follow up: [N] (pending ITC: Rs.X)
```

## Step 6 — Action Items

```
ACTION ITEMS:
1. [N] invoices in GSTR-2B not in books → Book these purchases before filing
2. [N] vendors to follow up for GSTR-1 filing → Emails drafted above
3. Rs.[X] blocked credit identified → Remove from ITC claim
4. Rs.[X] time-barred ITC → Do NOT claim
5. Rs.[X] amount mismatches → Raise credit/debit notes or get corrected invoices
```

This reconciliation is ready for CA review. After approval, use the ITC figures in the GSTR-3B review skill.
