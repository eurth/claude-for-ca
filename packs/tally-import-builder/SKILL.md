---
name: tally-import-builder
description: Build Tally XML from extracted registers. Download only — never live post.
---

# Tally import file

Convert the purchase register (and bank ledger if present) in reusable artifacts into Tally voucher mappings.

Confirm ledger names: Purchase A/c (Local/Interstate), CGST Input, SGST Input, IGST Input, party as Sundry Creditors, bank ledger from context.

The application will generate the XML file. You must still return a short validation summary: voucher count, total debit, GST totals, any unmapped parties.

Set approval.kind to tally_write.
Never say the vouchers have been posted. Staff will import via Tally Gateway → Import Data after Partner approval.
