---
name: fee-tracker
description: >
  Track fees billed and collected for all clients. Identify outstanding invoices,
  flag long-overdue collections, and provide a firm-level WIP (Work in Progress) summary.
  Helps the CA partner review billing status at any point in the month.
when_to_use: >
  To see a firm-level fee billing and collection summary, identify which clients
  have outstanding fees, or review WIP at month-end.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
  - Read
---

# Fee Tracker — Practice Management

**FINANCIAL INTEGRITY**: Unbilled WIP represents revenue not yet invoiced. Outstanding debtors represent invoiced but uncollected fees. Both must be reviewed regularly — ageing of debtors beyond 90 days is a collection risk.

## Fee Register Template

Maintain or ask the user to provide a fee register with:
- Client Name
- Engagement type
- Fee agreed (per engagement letter)
- Invoice date + Invoice number
- Invoice amount (+ GST)
- Amount collected
- Outstanding

```
FEE REGISTER — [Month] [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client       | Engagement    | Invoice  | Amount  | Collected | Outstanding | Days
XYZ Ltd      | Audit FY25-26 | INV-0041 | 1,18,000| 59,000    | 59,000      | 45
ABC Pvt Ltd  | GST Monthly   | INV-0042 | 11,800  | 11,800    | Nil         | —
PQR Traders  | Tax Audit 25  | INV-0043 | 59,000  | Nil       | 59,000      | 62 ⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total billed this month : Rs.X,XX,XXX
Total collected         : Rs.X,XX,XXX
Total outstanding       : Rs.X,XX,XXX (N invoices)
Overdue > 60 days       : Rs.XX,XXX (N invoices — follow up needed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Collection Follow-up Template

For overdue invoices, draft a reminder email:

```
Subject: Fee Outstanding — [Firm Name] | Invoice [INV-XXXX]

Dear [Client Contact],

We hope you are doing well. This is a gentle reminder regarding our professional
fee invoice [INV-XXXX] dated [date] for [services rendered], amounting to
Rs.[X] including GST.

As per our records, the above amount remains outstanding as on [date]. We request
you to arrange payment at your earliest convenience.

Bank details:
  Account Name: [CA Firm Name]
  Bank: [Bank] | Branch: [Branch]
  A/c No.: [XXXXXXXXXX] | IFSC: [XXXXXXXXXX]

Please share the payment proof / UTR number after payment.

Warm regards,
[CA Name]
[Firm Name]
```
