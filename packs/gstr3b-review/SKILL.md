---
name: gstr3b-review
description: Review GSTR-3B before filing. Draft working only.
---

# Review GSTR-3B

**FINANCIAL INTEGRITY:** Computation and checklist only. Do not submit. Cash-ledger payments need separate confirmation.

Use the selected GSTIN and period from context. Reuse purchase_register / sales_register / gstr2b if present.

## Section 3.1 outward

Taxable, zero-rated, nil/exempt, RCM inward, non-GST. Cross-check GSTR-1 totals; flag difference > Rs.100.

## Section 4 ITC

From GSTR-2B. Blocked credits s.17(5): motor vehicles (exceptions), food/catering, beauty/health, club, motor insurance (exceptions), rent-a-cab, construction, works contract for immovable property, personal, lost/stolen/gift.

Rule 42 mixed use: D1 = Total ITC × Exempt / Total turnover.
Rule 43 capital goods: 5% p.a. if mixed.

## Cash vs credit

Tax payable = output − net ITC. State cash required. Interest s.50 if late.

Output artifact `gstr3b_working` with tables and flags. Set approval.kind to gst_filing.
Always say this is a draft for the signing CA.
