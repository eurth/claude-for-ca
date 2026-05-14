---
name: review
description: Client onboarding dispatcher — overview and skill navigator
when_to_use: Start of a client onboarding workflow
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_firm_profile
---

# Client Onboarding — Dashboard

## Onboarding Workflow

```
NEW CLIENT ONBOARDING STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: KYC Documents Collection    → /client-onboarding:kyc-checklist
Step 2: Draft Engagement Letter     → /client-onboarding:engagement-letter
Step 3: Get EL signed + advance fee paid
Step 4: Register in memory bank     → /cold-start:add-client
Step 5: Set up compliance calendar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available Skills

```
/client-onboarding:kyc-checklist    → KYC documents checklist + PMLA compliance
/client-onboarding:engagement-letter → SA-210 engagement letter + fee structure
```
