---
name: annual-compliance
description: >
  Complete annual ROC compliance workflow — prepare agenda for AGM/EGM, draft notice,
  prepare directors' report, and ensure all annual forms are filed. Covers AGM requirements
  under Companies Act 2013, contents of Directors' Report (Section 134), and
  compliance for private limited and public companies.
when_to_use: >
  During the annual compliance season (June-September) when preparing for AGM,
  drafting directors' report, or filing annual returns.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Annual ROC Compliance

**FINANCIAL INTEGRITY**: Directors' Report is a statutory document signed by directors. All disclosures under Section 134 must be complete and accurate. Incorrect or incomplete directors' report can lead to personal liability for directors.

## AGM Notice — Mandatory Contents

Minimum 21 clear days' notice (unless shorter notice agreed by members holding ≥ 95% voting rights):

```
NOTICE
NOTICE is hereby given that the [Xth] Annual General Meeting of the Members of
[Company Name] (CIN: [XXXXXXXX]) will be held on [Day], [Date], at [Time], at
[Registered Office Address / VC/OAVM if permitted], to transact the following business:

ORDINARY BUSINESS:
1. To receive, consider and adopt the Audited Financial Statements (including Consolidated,
   if applicable) for the financial year ended 31st March 202X.
2. To declare Dividend of Rs.[X] per equity share (if applicable).
3. To appoint a Director in place of [Name] [DIN], who retires by rotation and being
   eligible, offers himself for re-appointment.
4. To ratify/appoint Statutory Auditors M/s [Firm] and fix their remuneration.

SPECIAL BUSINESS:
5. [Any special resolution items with explanatory statement]

By Order of the Board,
[Company Secretary / Director]
[Date]
```

## Directors' Report — Section 134 Checklist

| Disclosure | Section | Status |
|---|---|---|
| Extract of Annual Return (MGT-9) | 134(3)(a) | Required |
| Number of Board meetings | 134(3)(b) | Required |
| Directors' Responsibility Statement | 134(5) | Required |
| Declaration of Independent Directors | 149(6) | Required (if applicable) |
| Particulars of loans/guarantees/investments (S.186) | 134(3)(g) | Required |
| Related party transactions (Form AOC-2) | 134(3)(h) | Required |
| Conservation of energy, technology absorption | 134(3)(m) | Required (manufacturing) |
| Foreign exchange earnings and outgo | 134(3)(m) | Required |
| Risk management policy | 134(3)(n) | For listed + others |
| Corporate Social Responsibility (CSR) | 134(3)(o) | If CSR applicable |
| Statement on formal evaluation of Board | 134(3)(p) | Listed companies |
| Remuneration details (Section 197(12), Rule 5) | 197(12) | Required |
| Details of employees drawing > Rs.1.02 Cr p.a. | Rule 5(2) | If any |

## Directors' Responsibility Statement (Section 134(5))

```
Pursuant to the requirements of Section 134(5) of the Companies Act, 2013, your
Directors state that:

(a) in the preparation of the annual accounts, the applicable accounting standards
had been followed along with proper explanation relating to material departures;

(b) the directors had selected such accounting policies and applied them consistently
and made judgments and estimates that are reasonable and prudent so as to give a true
and fair view of the state of affairs of the Company at the end of the financial year
and of the profit and loss of the Company for that period;

(c) the directors had taken proper and sufficient care for the maintenance of adequate
accounting records in accordance with the provisions of this Act for safeguarding
the assets of the Company and for preventing and detecting fraud and other irregularities;

(d) the directors had prepared the annual accounts on a going concern basis;

(e) the directors had laid down internal financial controls to be followed by the Company
and that such internal financial controls are adequate and were operating effectively; and

(f) the directors had devised proper systems to ensure compliance with the provisions
of all applicable laws and that such systems were adequate and operating effectively.
```
