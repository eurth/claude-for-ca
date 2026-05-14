---
name: notice-analysis
description: >
  Read and analyse income tax notices (Section 142(1), 143(1), 143(2), 143(3), 144,
  147/148, 148A, 154, 156, 245, 271, 279). Explains in plain language, identifies the
  specific issue, calculates response deadline, drafts a structured reply, and advises
  on appeal rights and limitation periods.
when_to_use: >
  When a client receives any income tax notice or intimation — CPC intimation 143(1),
  scrutiny notices, reassessment notices 148/148A, demand notices 156, or penalty notices.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__log_notice
  - mcp__memory_bank__update_notice_status
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Income Tax Notice Analysis

**FINANCIAL INTEGRITY**: Tax notices have strict reply deadlines — missing them can lead to ex-parte assessment (best judgment), interest, and penalty. All drafts must be reviewed by the CA before submission. Never pay demand amounts without verifying with original return and CA.

## Notice Type Reference

| Section | Notice / Order | Nature | Typical Response Time |
|---|---|---|---|
| 143(1) | Intimation / Adjustment | CPC auto-processing differences | Objection within 30 days |
| 142(1) | Scrutiny — Produce documents | Limited/full scrutiny | As specified |
| 143(2) | Notice for Scrutiny Assessment | Scrutiny initiation | First hearing date |
| 143(3) | Assessment Order | Final scrutiny order | Appeal within 30 days |
| 144 | Best Judgment Assessment | Non-compliance | Appeal within 30 days |
| 147 | Income Escaped Assessment | Reassessment | — |
| 148 | Notice for Reassessment | Serve return | Within 3 months |
| 148A | Inquiry before 148 | Show cause why 148 needed | Within 7-14 days |
| 154 | Rectification of Mistake | Apparent mistake in order | Application within 4 years |
| 156 | Notice of Demand | Tax demand payment | 30 days for payment |
| 245 | Set-off of Refund | Refund adjusted against old demand | Objection within 30 days |
| 270A | Penalty | Under-reporting / misreporting | 30 days |
| 279 | Prosecution sanction | Criminal prosecution | Immediate — engage advocate |

## Step 1 — Parse the Notice

Ask the user to share:
- Full text of the notice (attach PDF or paste text)
- Date of notice + date received
- DIN number (mandatory on all notices post Oct 2019)

Immediately check:
- [ ] DIN present on the notice? (Notices without DIN issued after Oct 2019 are invalid)
- [ ] Notice served within limitation period?

## Step 2 — Plain Language Explanation

```
NOTICE SUMMARY — [Client] | PAN: [PAN]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Notice Type: Section [XX] — [Name]
Issued By: [AO / CPC / Jurisdictional AO]
Date of Notice: [date]
DIN: [XXXXXXXXXX] (VALID ✓ / ABSENT ⚠)
Reply Deadline: [date] — [N] days remaining

WHAT THE DEPARTMENT IS SAYING (plain language):
The Income Tax Department is [specific action: e.g. asking for documents /
questioning a deduction / making a demand / seeking your response before reopening].

SPECIFIC ISSUE RAISED:
[e.g. "Your GSTR-3B shows turnover of Rs.45L but ITR-3 shows Rs.42L — explain Rs.3L difference"]
[e.g. "Deduction u/s 80C of Rs.1.5L claimed but 26AS shows LIC premium of only Rs.75,000"]
[e.g. "Income of Rs.8.5L escaped assessment — interest income from FD not declared"]

AMOUNT IN DEMAND (if any): Rs.[X]
Interest u/s 234A/B/C (if any): Rs.[X]
Penalty proposed (if any): Rs.[X]
TOTAL DEMAND: Rs.[X]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 3 — Limitation Period Check (Reassessment Notices)

For Section 148 / 148A notices, check time limits:

| Income Escaped | From Which Year | Limitation (from end of AY) |
|---|---|---|
| < Rs.50 Lakh | All years | 3 years |
| ≥ Rs.50 Lakh | All years | 10 years |

If notice is time-barred: this is a strong defence — document and raise in reply.

## Step 4 — Legal Basis Analysis

For each issue raised:
- What section is the AO invoking?
- Is the legal basis correct?
- Are there favourable ITAT / High Court / Supreme Court rulings?
- Is the issue merely a mismatch (no actual additional income)?

## Step 5 — Draft Reply

```
[Firm Letterhead]
Date: [date]

To,
[DCIT / ACIT / ITO / CPC, Bengaluru / Jurisdictional AO]
[Address / online submission via e-proceedings]

PAN: [PANXXXXXXXX]
Assessment Year: [AY XXXX-XX]
Name: [Client Full Name]

Sub: Reply to Notice u/s [XX] dated [date] | DIN: [XXXXXXXX]

Respected Sir/Madam,

With reference to your notice dated [date] (DIN: [X]), I/we hereunder submit our reply:

PARA 1: BACKGROUND
[Client Name] (PAN: [PAN]) is a [individual / company / firm] earning income
primarily from [sources]. The ITR for AY [AY] was filed on [date] declaring
Total Income of Rs.[X].

PARA 2: ISSUE RAISED BY THE DEPARTMENT
[Restate issue clearly in your own words]

PARA 3: OUR EXPLANATION
[Detailed explanation with documentary evidence]

Point 1: [specific point]
→ Explanation: [factual explanation]
→ Evidence: Annexure [A] — [document name]

PARA 4: LEGAL POSITION
[Cite sections, circulars, case laws if applicable]

PARA 5: CONCLUSION
Based on the above, we respectfully submit that [the demand / addition / issue raised]
is [not warranted / incorrect / partially correct]. We request that the notice be
[dropped / demand be revised to Rs.X].

Enclosures:
Annexure A — [document]
Annexure B — [document]

Yours faithfully,
[CA Name] | M.No. [XXXXXX]
[Firm Name] | [Date]
```

## Step 6 — Register in Memory Bank + Action Plan

Call `mcp__memory_bank__log_notice` to register this notice.

```
ACTION PLAN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. URGENT: Gather documents listed in Annexures
2. Review draft reply with client — confirm facts are accurate
3. File reply via e-proceedings portal by [deadline]
4. If demand: DO NOT pay automatically — verify with original ITR first
5. If demand valid: Pay via Challan 280 (Self-Assessment Tax) to stop interest
6. If appeal required: File Form 35 (ITAT) within 30 days of order
7. Consider: Rectification u/s 154 if it's a CPC processing error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
