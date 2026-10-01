---
name: notice-triage
description: Analyse GST or income-tax notices and draft a reply for CA review.
---

# Notice (GST or income tax)

**FINANCIAL INTEGRITY:** Draft only. Must be signed by the authorised CA/advocate before sending. Never mark as replied. Never advise paying a demand without verifying books.

Detect portal from the document: GST (DRC-01, SCN, ASMT-10, ADJ, s.70 summons) vs Income-tax (142(1), 143(1)/(2)/(3), 144, 147/148/148A, 154, 156, 270A, 279).

Check DIN (mandatory after Oct 2019). Compute reply deadline.

Explain in plain language: what the department is saying, amounts, interest, penalty.

Draft a formal reply on firm letterhead tone with placeholders for facts not in the file.

Output `notice_summary` and `draft_reply`. Set approval.kind to notice_send.
