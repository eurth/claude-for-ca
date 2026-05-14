---
name: workpaper-draft
description: >
  Draft standard audit working papers — lead schedules, working trial balance,
  memo on significant accounting policies, contingent liability memo, related party
  disclosure checklist, representation letter, and audit completion checklist.
when_to_use: >
  During audit fieldwork to create structured working papers, or at audit completion
  to draft the audit completion memo and management representation letter.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Audit Working Papers

**FINANCIAL INTEGRITY**: Working papers are the auditor's primary evidence. They must be complete, cross-referenced, and signed off. All working papers are confidential and must be retained for the period specified under SA-230 (typically 7 years minimum).

## Working Paper Types

Use `$ARGUMENTS` to specify which working paper to draft:
- `lead-schedule` — Area-specific lead schedule (Revenue, Purchases, Fixed Assets, etc.)
- `trial-balance` — Working trial balance with audit adjustments
- `policies-memo` — Significant accounting policies memo
- `contingency-memo` — Contingent liabilities and commitments memo
- `related-party-checklist` — AS-18 / Ind AS 24 related party disclosure checklist
- `representation-letter` — Management representation letter (SA-580)
- `completion-checklist` — Audit completion checklist

---

## Lead Schedule Template

```
LEAD SCHEDULE — [AREA: Revenue / Purchases / Debtors / Fixed Assets etc.]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client: [Name] | FY: [FY] | WP Ref: [A/B/C-XX]
Prepared by: [Staff] | Date: | Reviewed by: [CA] | Date:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    Current Year   Prior Year    Variance    %Var
Ledger balance per TB Rs.X,XX,XXX  Rs.X,XX,XXX  Rs.XX,XXX   X%
Audit adjustments:
  (1) [Dr/Cr description] ± Rs.X,XXX
  (2) [Dr/Cr description] ± Rs.X,XXX
Audited amount     Rs.X,XX,XXX  Rs.X,XX,XXX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cross-references: → [Sub-schedule A1], → [Sub-schedule A2]
Tickmarks:
  ✓ = Agreed to financial statements
  ^ = Agreed to prior year audit WP
  @ = Agreed to supporting schedule
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Management Representation Letter (SA-580)

```
[Company Letterhead]
Date: [date]
To,
M/s [Audit Firm]
[Address]

Dear Sir/Madam,
Re: Audit of Financial Statements for the year ended 31st March 202X

In connection with your audit of the financial statements of [Company Name] for the year ended 31st March 202X, we confirm, to the best of our knowledge and belief, the following representations:

1. GENERAL
   (a) We have fulfilled our responsibilities for the preparation and presentation of the financial statements in accordance with [Ind AS / AS] as applicable.
   (b) We have provided you with all information relevant to the preparation of the financial statements.
   (c) All transactions have been recorded and reflected in the financial statements.

2. FRAUD AND IRREGULARITY
   (a) We acknowledge our responsibility for the design, implementation and maintenance of internal controls to prevent and detect fraud and error.
   (b) [Either:] We are not aware of any fraud or suspected fraud affecting the entity. [Or:] We have disclosed all known or suspected instances of fraud.

3. COMPLIANCE WITH LAWS
   We have complied with all aspects of contractual agreements that would have a material effect on the financial statements in the event of non-compliance.

4. RELATED PARTIES (AS-18 / Ind AS 24)
   We have disclosed all related party relationships and transactions. The related party disclosures in the financial statements are complete.

5. CONTINGENT LIABILITIES AND COMMITMENTS
   All known contingent liabilities, commitments, and guarantees have been disclosed in the financial statements. There are no claims against the company of which we are aware that have not been disclosed.

6. SUBSEQUENT EVENTS
   All events occurring subsequent to the date of the financial statements which require adjustment or disclosure have been adjusted/disclosed.

7. GOING CONCERN
   We believe that the company will continue to operate as a going concern for the foreseeable future.

Yours faithfully,
[Director Name] [Designation]
[Director Name] [Designation]
```

## Audit Completion Checklist

```
AUDIT COMPLETION CHECKLIST — [Client] | FY: [FY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLANNING
[ ] Engagement letter signed (SA-210)
[ ] Independence confirmation obtained (all team members)
[ ] Materiality set and documented
[ ] Risk matrix prepared and signed off (SA-315)
[ ] Audit programme completed and signed off

FIELDWORK
[ ] All planned procedures completed
[ ] All exceptions > performance materiality documented + resolved
[ ] CARO 2020 checklist completed (if applicable)
[ ] All related party disclosures verified
[ ] Tax audit 3CD completed (if applicable)
[ ] Stock verification performed
[ ] Bank confirmations obtained (or documented why not)
[ ] Debtors/creditors circularisation completed
[ ] Contingent liability legal letters obtained

COMPLETION
[ ] Unadjusted misstatements schedule reviewed by partner
[ ] Going concern assessment completed (SA-570)
[ ] Subsequent events review performed (up to report date)
[ ] Management representation letter signed
[ ] EQCR review completed (listed / public interest entities)
[ ] SA-700/705/706 — report type finalised
[ ] Audit report signed and dated
[ ] Final accounts initialled by director + auditor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
