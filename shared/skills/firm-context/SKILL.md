---
name: firm-context
description: Load the firm's profile, upcoming due dates, and pending notices from the offline memory bank into the current context. Run this at the start of any CA work session to give Claude full awareness of the firm's situation.
when_to_use: At the start of any compliance, audit, or client work session. Invoke manually with /claude-for-ca-core:firm-context if the session context was not loaded automatically.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_firm_profile
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__list_notices
  - mcp__memory_bank__get_due_dates
---

# Firm Context Loader

You are loading the CA practice context from the offline memory bank to set up this work session.

## Step 1 — Load Firm Profile

Call `mcp__memory_bank__get_firm_profile`. If the profile is not configured, stop and tell the user to run `/cold-start:onboard-firm` first.

## Step 2 — Load Upcoming Due Dates

Call `mcp__memory_bank__get_due_dates` with `days_ahead: 30`. Group results by urgency:
- **This week (7 days):** highlight in bold
- **This fortnight (8–14 days):** normal
- **This month (15–30 days):** listed below

## Step 3 — Load Pending Notices

Call `mcp__memory_bank__list_notices` with `status: "received"` and `status: "in_progress"`. List any open notices grouped by client.

## Step 4 — Present Summary

Present a clean session briefing in this format:

---
**CA Practice Session — [Firm Name]**
Partner: [CA Name] | GSTIN: [GSTIN] | Jurisdiction: [Jurisdiction]

**Due This Week:**
[table of form / client / due date]

**Pending Notices:**
[list: client — section — due date — demand]

**Memory Bank:** [N] clients | [N] open tasks | [N] open notices
---

End with: "Financial integrity guardrails are active. All filings and Tally writes require your explicit approval."
