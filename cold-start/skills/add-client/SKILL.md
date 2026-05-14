---
name: add-client
description: Add a new client to the memory bank registry. Collects client details interactively and saves to SQLite. Use anytime a new client engagement begins.
when_to_use: When onboarding a new client to the firm. Invoke with /cold-start:add-client
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__save_client
  - mcp__memory_bank__log_compliance_event
---

# Add New Client

Collect client details in a single structured conversation.

## Step 1 — Collect Details

Ask for all of the following at once:

1. **Entity / client name** (full legal name)
2. **PAN** (10-character alphanumeric)
3. **GSTIN** (if GST-registered, 15 characters; or "Not registered")
4. **TAN** (if deductor, 10 characters; or "Not applicable")
5. **CIN** (for companies/LLPs; or "Not applicable")
6. **Entity type** — Individual / HUF / Partnership / LLP / Private Ltd / Public Ltd / Trust / AOP / Other
7. **Industry** — brief description (e.g. "Cotton yarn trading")
8. **Jurisdiction** — state
9. **Contact person** — name, email, phone
10. **Tally company name** — as it appears in Tally (or "Not on Tally")
11. **Notes** — any special instructions (e.g. "Files on composition scheme", "MSME registered", "Foreign subsidiary")

## Step 2 — Check for Duplicate

Call `mcp__memory_bank__get_client` with the provided PAN (and GSTIN if given) to check for an existing record. If found, ask: "A client with this PAN already exists: [name]. Do you want to update their record or create a new one?"

## Step 3 — Save Client

Generate a `client_id` as snake_case of the entity name, max 20 characters, unique. Call `mcp__memory_bank__save_client`.

## Step 4 — Set Up Compliance Calendar (Optional)

Ask: "Which recurring filings should I track for [client name]?" Present a quick checklist:
- GST (GSTR-1 + 3B — monthly or quarterly?)
- TDS returns (24Q/26Q?)
- ITR (which form and assessment year?)
- Tax Audit (3CA/3CB + 3CD?)
- ROC (AOC-4, MGT-7?)

For each selected, create a calendar entry for the current period with `mcp__memory_bank__log_compliance_event`.

## Step 5 — Confirm

"✓ Client **[name]** (PAN: [pan]) added to the registry with [N] compliance calendar tasks."
