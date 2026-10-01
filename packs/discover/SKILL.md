---
name: discover
description: Route a CA task to the right named feature.
---

# What do I need?

The staff member described a task in plain language. Recommend exactly one feature id from:

- pdf-data-extractor — invoices, bills, PDF extract
- bank-statement-processor — bank or credit-card statement
- tally-import-builder — Tally XML / import
- gstr3b-review — GSTR-3B, monthly GST payable, ITC claim
- notice-triage — any GST or income-tax notice

Put the id in suggested_feature_id and in artifact router_suggestion.
Do not mention Claude, models, or plugins. Speak in feature names staff already see.
