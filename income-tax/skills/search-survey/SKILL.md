---
name: search-survey
description: >
  Assistance for clients facing Income Tax Search (Section 132) or Survey (Section 133A/133B).
  Explains rights, what to do during search/survey, document preservation, post-search
  compliance (filing statement u/s 132(4), filing revised ITR), and settlement options.
when_to_use: >
  When a client calls saying there is a search or survey happening at their premises,
  or after a search/survey when they need to understand next steps and compliance.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__log_notice
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Search & Survey — Emergency Assistance

**FINANCIAL INTEGRITY**: Search (Section 132) and Survey (Section 133A) are serious statutory proceedings. All guidance must be reviewed by an advocate/CA specialist. Nothing said during search without CA/advocate present should be treated as final admission. This assistant provides general guidance — always engage a qualified representative immediately.

## IMMEDIATE — Search (Section 132) in Progress

If the client calls during a live search:

```
IMMEDIATE GUIDANCE FOR SEARCH (Section 132):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. STAY CALM — Do not panic or attempt to destroy/hide documents
2. VERIFY AUTHORITY — Request to see the Search Warrant under Section 132(1)
   - Contains: DIN, assessee name, authorised officer's name, jurisdiction
   - If no warrant shown → do not allow entry, call CA immediately
3. CALL YOUR CA / ADVOCATE IMMEDIATELY — Do not answer questions alone
4. DO NOT SIGN ANYTHING until CA/advocate is present
5. COOPERATE WITHIN LIMITS — Do not obstruct search; do not surrender more than required
6. KEEP TRACK of all documents taken, digital devices seized
7. FOOD / MEDICATION for family — officers must allow reasonable access
8. DO NOT transfer funds or move assets during search — Sec 132(3) can freeze
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Section 132 vs Section 133A — Differences

| Feature | Search (Sec 132) | Survey (Sec 133A) |
|---|---|---|
| Warrant | Required (search warrant) | Not required |
| Timing | Day + night (can continue) | Business hours only |
| Seizure | Can seize documents, assets, cash | Cannot seize assets/cash |
| Cash find | Can seize unexplained cash | Can impound documents only |
| Premises | Residence + business | Business premises only |
| Duration | Can last days | Typically single day |

## Survey (Section 133A) — Rights and Obligations

During a survey at business premises:
- Officers may enter during business hours without warrant
- They can inspect books, documents, verify stocks
- **They CANNOT take custody of documents or cash** (only impound temporarily for copying)
- You must explain cash in hand at business premises
- Stock should be verifiable from books

## Post-Search Compliance

### Within 60 Days of Search
File Statement u/s 132(4) if the AO calls:
- Admit or deny any undisclosed income found
- This is a sworn statement — accuracy is critical
- **Always done with CA/advocate present**

### Filing Post-Search Return
Within 30 days of last date of return of seized documents, file:
- Any pending ITRs (undisclosed income years)
- Statement of undisclosed income declared under Block Assessment (Section 132B)

### Settlement Options
1. **Voluntary Disclosure**: Declare undisclosed income in Section 132(4) statement
   - Pay tax + 30% surcharge + 4% cess
   - No penalty if disclosure is complete
2. **Settlement Commission**: File application (discontinued from 2021, cases pending only)
3. **Vivad Se Vishwas**: If demand raised post-search, settle at reduced rates
4. **Fight the demand**: Contest in Assessment proceedings → CIT(A) → ITAT

### Block Assessment (Section 153A)
After search: AO will issue notice u/s 153A to file ITR for last 6 AYs.
- All 6 years (+ year of search) re-opened
- Any undisclosed income: Tax @ 60% + surcharge 25% + cess 4% = effective ~78%
- Penalty: 30% of undisclosed income (if not voluntarily disclosed)

## Document Preservation

Ask the CA to immediately preserve:
- [ ] All bank statements (last 6 years)
- [ ] All ITRs filed (with acknowledgements)
- [ ] Tally data backup (current and archived)
- [ ] Property documents, investment records
- [ ] Business contracts, purchase orders
- [ ] Loan documents
- [ ] Explanation for any large cash transactions

## CA's Role

The CA must:
1. Be present or arrange a representative immediately
2. Ensure a Mahazar (seizure memo) is signed — list all seized items
3. Apply for return of seized documents (Section 132B — within 60 days no interest, after that 15% p.a. interest for delay in seizure)
4. Ensure no voluntary statement is given without legal advice
5. File a complaint if officers exceed their authority
