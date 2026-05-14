---
name: engagement-letter
description: >
  Draft Engagement Letter and Terms of Engagement as required by SA-210 (Agreeing
  the Terms of Audit Engagements). Covers statutory audit, tax audit, GST audit,
  internal audit, accounting, and advisory engagements. Includes scope, fee, billing
  terms, client responsibilities, and limitation of liability clauses.
when_to_use: >
  When onboarding a new client for any engagement. Draft the engagement letter
  before starting any work — this is mandatory for statutory audits per SA-210.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__add_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Engagement Letter — SA-210

**FINANCIAL INTEGRITY**: SA-210 requires that engagement terms be agreed in writing before commencing statutory audit. Without a signed engagement letter, the firm's scope and liability are undefined. Always get the engagement letter signed before starting work.

## Engagement Letter Template

Use `$ARGUMENTS` to specify engagement type: `statutory-audit`, `tax-audit`, `gst-advisory`, `accounting`, `advisory`

---

### Statutory Audit Engagement Letter

```
[CA FIRM LETTERHEAD]
Date: [date]

To,
The Board of Directors,
[Company Name],
[Registered Address]

Dear Sir/Madam,

LETTER OF ENGAGEMENT — STATUTORY AUDIT FOR FY [FY]

We are pleased to confirm our appointment as Statutory Auditors of [Company Name]
(hereinafter "the Company") for the financial year ending 31st March [YYYY], as
resolved at the [Annual General Meeting / Extraordinary General Meeting] held on [date].

1. OBJECTIVE AND SCOPE OF AUDIT
   The objective of our audit is to express an opinion on the financial statements
   of the Company whether they give a true and fair view in conformity with the
   accounting standards (Ind AS / AS applicable) and the Companies Act, 2013.
   
   Our audit will be conducted in accordance with the Standards on Auditing (SAs)
   issued by the Institute of Chartered Accountants of India (ICAI).

2. MANAGEMENT'S RESPONSIBILITIES
   The management of the Company is responsible for:
   (a) Preparation of financial statements that give a true and fair view
   (b) Maintenance of adequate accounting records
   (c) Safeguarding of assets and prevention of fraud
   (d) Providing us with all information and explanations we deem necessary

3. AUDITORS' RESPONSIBILITIES
   Our responsibility is to express an opinion on the financial statements based
   on our audit. We will conduct the audit in accordance with SAs and comply with
   all ethical requirements including independence requirements.
   
   Our audit does not relieve management of its responsibilities.
   
   We may discuss matters with management and the Board of Directors / Audit Committee
   as required by the Standards on Auditing.

4. REPORTING
   We will issue our Audit Report in accordance with:
   - SA-700 (Forming an Opinion and Reporting on Financial Statements)
   - SA-705 (Modifications to the Opinion in the Independent Auditor's Report) — if applicable
   - SA-706 (Emphasis of Matter and Other Matter Paragraphs) — if applicable
   - CARO 2020 (if applicable)

5. PROFESSIONAL FEES
   Our professional fees for the audit are fixed at Rs.[X,XX,XXX] plus applicable
   GST @ 18%. Fees are payable as follows:
   - 50% advance on commencement of audit
   - Balance on delivery of signed audit report
   
   Out-of-pocket expenses (travel, printing, etc.) will be billed at actuals.
   
   The fees are subject to revision if the scope of work increases materially.

6. CONFIDENTIALITY
   We will maintain confidentiality of all information obtained during the audit
   and will not disclose it to third parties except as required by law or
   professional standards.

7. DATA PROTECTION
   Client data accessed during the audit will be stored securely and will not
   be retained beyond the period required by professional standards.

8. LIMITATION OF LIABILITY
   Our liability arising from this engagement is limited to direct losses caused
   by our negligence and shall not exceed [X times] our professional fees for
   the relevant engagement.

Please confirm your acceptance of the terms of this engagement by signing and
returning the duplicate copy of this letter.

We look forward to a productive professional relationship with your Company.

Yours faithfully,
For [CA Firm Name]

[Partner Name]
Partner | M.No.: [XXXXXX]
[ICAI Firm Reg. No.: XXXXXXW]


ACCEPTANCE:

We, on behalf of [Company Name], accept the terms of engagement set out above.

Signed: ____________________
Name: ______________________
Designation: ________________
Date: ______________________
```

---

### Other Engagement Types

For **Tax Audit (3CD)**: Similar structure; add scope = "Form 3CA/3CB and 3CD"; fee = Rs.[X]

For **Accounting/Monthly Bookkeeping**: Scope = "Maintenance of books of accounts in Tally"; frequency = monthly; fee = Rs.[X]/month.

For **GST Advisory**: Scope = GST filings (GSTR-1, GSTR-3B, reconciliation); retainer fee = Rs.[X]/month.
