---
name: gstr1-review
description: >
  Review GSTR-1 outward supply data before filing. Checks classification of supplies
  (B2B/B2C/exports/nil-rated/exempt), validates HSN summary, e-Invoice linkage, place
  of supply, and flags mismatches with the sales register. Covers both monthly and
  QRMP (IFF) filers.
when_to_use: >
  When the user wants to review GSTR-1 data before submission, check outward supplies,
  verify HSN codes, review IFF data, or reconcile GSTR-1 with sales register/e-invoices.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
  - mcp__memory_bank__get_due_dates
  - Read
  - Write
---

# GSTR-1 Review

**FINANCIAL INTEGRITY**: GSTR-1 review only. Do NOT file or submit until the partner has verified all items and triggered the GST Filing HITL approval step.

## Firm Context
!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null || echo "Run /cold-start:onboard-firm to set up firm profile"`

## Step 1 — Client and Period

Ask (if not provided):
- Client name / GSTIN
- Return period (Month-Year for monthly, Quarter for QRMP)
- Are they a QRMP filer? (IFF for first two months, quarterly GSTR-1 for Q3)

## Step 2 — Collect Source Data

Accept data in any format:
- Excel/CSV export from Tally or billing software
- Pasted table
- JSON from pdf-data-extractor skill

Or pull directly from GST portal:
- `mcp__gst_portal__get_gstr1_draft(gstin, period)` — fetches saved draft from portal

## Step 3 — Classification Review

For each supply, verify the correct table:

| Supply Type | GSTR-1 Table | Criteria |
|---|---|---|
| B2B Taxable | Table 4 | Registered buyer, GSTIN provided |
| B2C Large | Table 5 | Unregistered, invoice value > Rs.2.5L inter-state |
| B2C Small | Table 7 | Unregistered, invoice value ≤ Rs.2.5L |
| Zero-Rated Exports | Table 6A/6B | Export with/without LUT |
| Nil / Exempt / Non-GST | Table 8 | No tax charged |
| Reverse Charge | Table 4B | Services from unregistered dealers |
| Advances Received | Table 11A | Advance received, supply not made |
| Debit/Credit Notes | Tables 9/10 | CDN for B2B/B2C |

**Flag if:**
- Registered buyer invoice placed in B2C table (revenue leakage risk for buyer)
- GSTIN in Table 4 does not pass format validation (15 chars, state code, PAN-embedded)
- Place of supply does not match buyer's state (CGST+SGST vs IGST mismatch)

## Step 4 — HSN Summary Validation (Table 12)

For turnover > Rs.5 Cr: 6-digit or 8-digit HSN mandatory
For turnover Rs.1.5–5 Cr: 4-digit HSN mandatory  
For turnover < Rs.1.5 Cr: HSN optional but recommended

Check:
- [ ] All HSN codes are valid (cross-check against HSN master)
- [ ] HSN-level taxable value and tax amounts match sum of invoice details
- [ ] Unit of Measurement (UOM) is valid GST-approved UOM
- [ ] 8-digit HSN for pharma/chemicals/textiles (as notified)

## Step 5 — E-Invoice Reconciliation (for turnover > Rs.10 Cr)

If client is e-Invoice mandated (turnover > Rs.10 Cr w.e.f. 1 Apr 2023):
- [ ] Every B2B invoice above Rs.0 must have an IRN (Invoice Reference Number)
- [ ] IRN is 64-character hash
- [ ] E-way bill auto-generated for consignment value > Rs.50,000
- [ ] Cancel-and-reissue invoices have separate IRN with cancellation reason

Flag: Any B2B invoice without IRN for e-Invoice mandated taxpayer = portal rejection

## Step 6 — Summary Comparison

Pull GSTR-1 summary and compare with:
- Sales Register total (from Tally or accounting software)
- E-Invoice data (if applicable)
- Previous month's GSTR-1 (for unusual jumps)

Present comparison table:
```
GSTR-1 Review Summary — [Client Name] | GSTIN: [GSTIN] | Period: [Period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOURCE                 | TAXABLE VALUE   | CGST     | SGST     | IGST     | TOTAL
GSTR-1 Draft           | Rs.XX,XX,XXX    | Rs.X,XXX | Rs.X,XXX | Rs.X,XXX | Rs.XX,XXX
Sales Register (Tally) | Rs.XX,XX,XXX    | Rs.X,XXX | Rs.X,XXX | Rs.X,XXX | Rs.XX,XXX
Difference             | Rs.XX,XXX ⚠     | Rs.XX    | Rs.XX    | Rs.XX    | Rs.XX,XXX
```

## Step 7 — Exceptions List

Present all exceptions for CA review:
```
EXCEPTIONS REQUIRING YOUR REVIEW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ⚠ Invoice Nos. 45, 67: Registered buyer (GSTIN present) filed in B2C table
   → Move to B2B (Table 4) or confirm buyer is unregistered
2. ⚠ Invoice No. 89: IGST charged, both parties in AP (should be CGST+SGST)
   → Verify place of supply
3. ⚠ GSTR-1 taxable value Rs.2,34,000 > Sales Register Rs.2,31,500
   → 3 invoices appear in portal not in Tally — check for manual invoices
4. ⚠ HSN 85176990: Total value Rs.5,80,000 but tax @ 18% = Rs.1,04,400, portal shows Rs.1,02,000
   → Recalculate or check for non-taxable invoices in this HSN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 4 exceptions | After resolving, proceed to GSTR-3B review
```

## Step 8 — Due Date Reminder

- Monthly filer (normal): 11th of next month
- QRMP (IFF for Months 1 and 2): 13th of next month
- QRMP (Quarterly GSTR-1): 13th of first month after quarter
- Late filing: Rs.50/day (Rs.25 CGST + Rs.25 SGST) | NIL filer: Rs.20/day

```
DUE DATE REMINDER:
GSTR-1 for [Period]: Due [Date]
Days remaining: [N] days
Late fee (if filed on date): Rs.[X]
```
