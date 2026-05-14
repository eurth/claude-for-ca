---
name: notice-triage
description: >
  Parse and analyse GST notices (SCN/DRC-01/ASMT-10/ASMT-11/ADJ-01/RFD-09 and others).
  Explains demand in plain language, identifies the legal basis, calculates time remaining
  to reply, pulls prior return data for context, and drafts a structured reply.
when_to_use: >
  When a client receives a GST notice — DRC-01, SCN, ASMT-10, ADJ-01, audit notice,
  or any other notice from GST department. Also for summons under Section 70.
effort: high
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__log_notice
  - mcp__memory_bank__list_notices
  - mcp__memory_bank__update_notice_status
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# GST Notice Triage

**FINANCIAL INTEGRITY**: Legal responses to statutory notices carry serious consequences. Any draft response is for CA review ONLY and must be signed by the authorised CA/advocate before submission. Never mark a notice as "replied" until the actual reply is filed.

## Firm Context
!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null || echo "Run /cold-start:onboard-firm to set up firm profile"`

## Step 1 — Collect the Notice

Ask the user to:
- Attach/paste the full text of the notice, OR
- Share the key details: notice number, section, demand amount, DIN number, date received, due date for reply

## Step 2 — Notice Classification

Identify the notice type:

| Notice Type | Section | Nature | Reply Time |
|---|---|---|---|
| DRC-01 | Sec 73/74 | Tax demand (non-fraud / fraud) | 30 days |
| DRC-01A | Sec 73/74 | Pre-SCN communication | 30 days |
| ASMT-10 | Sec 61 | Scrutiny of returns — discrepancy | 30 days |
| ASMT-11 | Sec 62 | Best judgement assessment | — |
| ADJ-01 | Sec 63 | Non-filer assessment | — |
| SCN | Sec 74 | Show Cause Notice — tax evasion | 30 days |
| RFD-09 | Sec 54 | Refund rejection — show cause | 15 days |
| Form GST AUDIT-2 | Sec 65 | Department audit notice | 15 days |
| Summons | Sec 70 | Personal appearance required | As stated |
| ENQ-01 | Sec 67 | Inspection / search | Immediate |

## Step 3 — Plain Language Explanation

After reading the notice, explain to the CA:

```
NOTICE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Client: [Name] | GSTIN: [GSTIN]
Notice Type: [DRC-01 / ASMT-10 / SCN / etc.]
Reference No.: [DIN / Notice Ref]
Issued By: [Adjudicating Authority / CGST / SGST]
Date of Notice: [date]
Date Received: [date]
Reply Deadline: [date] ([N] days remaining)

WHAT THE DEPARTMENT IS SAYING (plain language):
The GST department is asking [client name] to explain [specific discrepancy/demand].

The specific issue raised is:
[Explain: e.g. "GSTR-3B for Oct-Dec 2024 shows ITC of Rs.5,40,000 but GSTR-2B shows only
Rs.4,20,000. The department wants to know why excess ITC of Rs.1,20,000 was claimed."]

Amount in Demand: Rs.[X]
Interest Proposed: Rs.[X] @ [18%/24%] from [date] to [date]
Penalty Proposed: Rs.[X]
TOTAL DEMAND: Rs.[X]

LEGAL BASIS:
Section [XX] of CGST Act — [brief description of section]
Notification / Circular: [if mentioned]
```

## Step 4 — Pull Prior Data

Using the memory bank and any available return data, pull context:
- GSTR-3B for the disputed period
- GSTR-2B for the disputed period
- Any prior notices for this client/period
- Any amendments filed

Identify the source of the discrepancy:
```
ROOT CAUSE ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Possible reasons for the discrepancy:
1. Vendor [Name] had reversed/amended their GSTR-1 after we claimed ITC
2. Time-barred ITC mistakenly claimed — Section 16(4) issue
3. Blocked credit (Section 17(5)) — [category]
4. Genuine mismatch due to [specific reason]
5. Data entry error in GSTR-3B

DOCUMENTS TO GATHER FOR REPLY:
[ ] Purchase invoices for the disputed period
[ ] GSTR-2B downloads for the period
[ ] Payment challans (if tax was already paid)
[ ] Correspondence with vendor regarding amendments
[ ] Auditor's working papers for ITC claim
```

## Step 5 — Draft Reply

Draft a formal reply to the notice. Use the following structure:

```
[Firm Letterhead]
Date: [reply date]

To,
The [Designated Officer / Superintendent / Commissioner]
[Office Address]

Sub: Reply to [Notice Type] bearing DIN [XXXXX] dated [date] — [Client Name] — GSTIN [GSTIN]

Ref: Your notice dated [date] ref. [notice no.] issued u/s [XX] of CGST Act 2017

Sir/Madam,

We, [CA Firm Name], authorized tax consultants for [Client Name] (GSTIN: [GSTIN]),
respectfully submit the following reply to the above-referenced notice.

1. BACKGROUND
[Client Name] is a [entity type] engaged in [business description] and duly registered
under GST with GSTIN [GSTIN]. The notice pertains to [period].

2. ISSUE RAISED
[Restate the specific issue from the notice clearly]

3. OUR EXPLANATION
[Detailed, factual explanation of each point raised]

4. SUPPORTING DOCUMENTS
Enclosed herewith:
Annexure A — [document description]
Annexure B — [document description]
...

5. CONCLUSION
Based on the above, we humbly submit that:
[State whether demand is correct / incorrect / partially correct]
[State action being taken if any tax is payable]

We are confident that on review of the above, the notice will be dropped / demand
will be reduced to Rs.[X].

We remain available for any further clarification.

Yours faithfully,

[CA Name]
[Membership No.]
[Firm Name]
[Date]
```

## Step 6 — Register Notice in Memory Bank

Log the notice so it appears on the compliance dashboard:

Call `mcp__memory_bank__log_notice` with:
- client_id, notice_type, section, reference_number, demand_amount, due_date, status: "open"

## Step 7 — Action Plan

```
ACTION ITEMS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Immediate] Gather supporting documents listed in Step 4
2. [By [date-5 days]] Review draft reply with client
3. [By [date-2 days]] File reply on GST portal (ASMT-11 / DRC-03 / as applicable)
4. [If demand valid] Make payment using DRC-03 within 30 days for immunity from penalty
5. [File in records] Save copy of notice + reply + acknowledgment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WARNING: Interest runs from the date of short payment / excess ITC.
Filing a DRC-03 for voluntary payment stops interest accrual from that date.
```
