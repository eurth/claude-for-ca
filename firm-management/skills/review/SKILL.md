---
name: review
description: >
  Firm management dispatcher — shows practice KPIs, pending invoices, staff utilization
  summary, and navigates to practice management skills.
when_to_use: >
  At start of week/month for practice management review, or to navigate to any
  firm management skill.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
  - mcp__memory_bank__get_due_dates
---

# Firm Management — Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## Available Firm Management Skills

```
/firm-management:fee-tracker    → Outstanding fees, collection status, reminder drafts
```

## Monthly Practice Review Checklist

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MONTHLY PRACTICE REVIEW — [Month] [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Fee billing complete for all completed work
[ ] Outstanding invoices > 60 days — follow up sent
[ ] Compliance calendar checked — any deadlines missed?
[ ] Staff timesheets reviewed (if applicable)
[ ] New client enquiries followed up
[ ] Engagement letters signed for all new engagements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
