---
name: review
description: Advisory CA dispatcher — overview and quick navigation
when_to_use: Start of an advisory session or to navigate to advisory skills
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# Advisory CA — Dashboard

## Available Advisory Skills

```
/advisory-ca:tax-planning     → Old vs new regime, 80C/80D planning, year-end checklist
/advisory-ca:msme-advisory    → Udyam registration, Section 43B(h), MSME-1, Samadhaan
```

## Common Advisory Queries

- "Which tax regime is better for my client?" → Use `/advisory-ca:tax-planning`
- "My client buys from MSMEs — are payments compliant?" → Use `/advisory-ca:msme-advisory`
- "Should my client register as MSME?" → Use `/advisory-ca:msme-advisory`
