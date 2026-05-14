---
name: review
description: >
  GST compliance dispatcher. Shows pending GST tasks for all clients, lets the CA
  quickly jump to any specific skill, and provides a daily/weekly GST dashboard.
when_to_use: >
  At the start of a session when you want a GST compliance overview, to see what's due
  this month, or to quickly access any GST skill. Use "/gst-compliance:review" for a
  morning dashboard.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_due_dates
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__list_notices
  - mcp__memory_bank__get_firm_profile
---

# GST Compliance Review — Daily Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## GST Calendar — This Month

Pull upcoming due dates from memory bank:

```
GST DUE DATES — [Current Month]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11th — GSTR-1 (Monthly filers)
13th — GSTR-1 (QRMP quarterly) / IFF (QRMP months 1 & 2)
20th — GSTR-3B (Monthly, non-QRMP)
22nd — GSTR-3B (QRMP — Category I states: AP, Telangana, etc.)
24th — GSTR-3B (QRMP — Category II states)
25th — PMT-06 (QRMP quarterly tax payment)
28th — GSTR-11 (UIN holders, if applicable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Client-wise Status

List clients with pending GST filings for this month.

## Available GST Skills

```
/gst-compliance:gstr1-review      → Review GSTR-1 before filing
/gst-compliance:gstr3b-review     → Review GSTR-3B + tax computation
/gst-compliance:itc-recon         → GSTR-2B vs Purchase Register reconciliation
/gst-compliance:notice-triage     → Parse and reply to GST notices
/gst-compliance:annual-return     → GSTR-9 and GSTR-9C preparation
/gst-compliance:gst-audit         → Department audit / special audit assistance
```

## Pending Notices

Show any open GST notices from memory bank with days remaining for reply.
