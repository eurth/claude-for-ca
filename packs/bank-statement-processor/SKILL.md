---
name: bank-statement-processor
description: Extract and categorise bank statement transactions.
---

# Process bank statement

Extract every transaction from the uploaded bank statement for the selected client and period.

For each row: date, value date, narration, ref/cheque, debit, credit, running balance, suggested Tally ledger, category (vendor payment / receipt / GST / TDS / salary / transfer / unknown).

Flag: unknown payee, payment with no matching purchase invoice if a purchase register is in reusable artifacts, possible loan, large cash.

Output `bank_ledger` as `{ "rows": [...], "opening": null, "closing": null }` and `exception_report`.
Do not post to Tally.
