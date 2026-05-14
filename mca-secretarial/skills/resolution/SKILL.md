---
name: resolution
description: >
  Draft board resolutions and shareholder resolutions for common corporate actions.
  Covers appointment/resignation of directors, change of auditor, bank mandate changes,
  dividend declaration, loans to related parties, property transactions, and more.
  Also drafts notices convening board meetings and general meetings.
when_to_use: >
  When a company needs to pass a board resolution or ordinary/special resolution at
  a general meeting. When drafting meeting notices or minutes of meetings.
effort: medium
model: claude-sonnet-4-6
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Board / Shareholder Resolutions

**FINANCIAL INTEGRITY**: Resolutions are legal corporate records. Incorrect resolutions (e.g., inadequate authority for loans to related parties) can create personal liability for directors. Certain resolutions must be filed with MCA within 30 days (MGT-14). Always verify Section references before use.

## Common Resolutions — Quick Pick

Use `$ARGUMENTS` to specify: e.g. "appointment of director", "bank mandate change", "loan to related party"

---

## Resolution Templates

### 1. Appointment of Additional Director (Section 161)

```
RESOLVED THAT pursuant to Section 161(1) of the Companies Act, 2013 and Article [XX] of the
Articles of Association of the Company, the consent of the Board be and is hereby accorded
to appoint [Name], [DIN: XXXXXXXX], as an Additional Director (Executive/Non-Executive/
Independent) of the Company, to hold office up to the date of the next Annual General Meeting.

RESOLVED FURTHER THAT [Authorised Signatory] be and is hereby authorised to sign and
file Form DIR-12 with the Registrar of Companies and do all acts, deeds and things as may
be necessary to give effect to the above resolution.
```

**MCA filing required**: DIR-12 (within 30 days)

---

### 2. Resignation of Director

```
RESOLVED THAT the resignation of [Name], [DIN: XXXXXXXX], as [Designation] of the Company,
tendered vide his/her letter dated [date], be and is hereby accepted with effect from [date].

RESOLVED FURTHER THAT [Authorised Signatory] be and is hereby authorised to file
Form DIR-12 with the Registrar of Companies within the prescribed time.
```

**MCA filing**: DIR-12 (within 30 days) + DIR-11 (by resigning director)

---

### 3. Appointment/Re-appointment of Statutory Auditor (Section 139)

```
RESOLVED THAT pursuant to Section 139(1) and other applicable provisions of the Companies
Act, 2013 and the Companies (Audit and Auditors) Rules, 2014, M/s [Firm Name], Chartered
Accountants, [ICAI Firm Registration No. XXXXXXW], be and are hereby appointed as the
Statutory Auditors of the Company, to hold office from the conclusion of this [_th] Annual
General Meeting until the conclusion of the [_th] Annual General Meeting, at a remuneration
of Rs.[X] per annum plus applicable taxes and reimbursement of out-of-pocket expenses.
```

**MCA filing**: ADT-1 (within 15 days of AGM)

---

### 4. Opening/Closing Bank Account (Bank Mandate)

```
RESOLVED THAT a [current / savings / cash credit / OD] account be opened with
[Bank Name], [Branch Name], [IFSC: XXXX].

RESOLVED FURTHER THAT the following persons be authorised to operate the said account:
1. [Name] — [Designation] — [Singly / Jointly]
2. [Name] — [Designation] — [Singly / Jointly]

RESOLVED FURTHER THAT the bank be informed of the above mandate and that any prior
mandate relating to the said bank account stand superseded.
```

**MCA filing**: Not required

---

### 5. Loan to Related Party (Section 185/186)

```
RESOLVED THAT pursuant to Section 185 and Section 186 of the Companies Act, 2013,
as amended, and subject to the approval of members (if required under Section 185/186),
the Board hereby approves the grant of a loan of Rs.[X] to [Related Party Name], on
the following terms:
  - Interest Rate: [X]% per annum (not less than prevailing RBI bank rate)
  - Repayment: [terms]
  - Purpose: [stated purpose]

RESOLVED FURTHER THAT the loan shall be utilised by [Related Party] only for the
purpose stated above and not for acquiring shares or for speculative purposes.

RESOLVED FURTHER THAT the requisite disclosures under Section 186 be made in the
financial statements.
```

**Note**: Section 185 loans to directors require shareholders' special resolution + other conditions. Section 186 loans may require approval if limits exceeded.

---

### 6. Dividend Declaration (Interim / Final)

**Interim Dividend (Board Resolution):**
```
RESOLVED THAT pursuant to Section 123 of the Companies Act, 2013, the Board hereby
declares an interim dividend of Rs.[X] per equity share (face value Rs.10) for the
financial year [FY], payable to all members as on the record date of [date].

RESOLVED FURTHER THAT the dividend be paid from the current year's profits and that
[CFO/Finance Head] be authorised to complete all formalities including opening of a
separate dividend account, transfer of amount, and filing of necessary forms.
```

**Note**: TDS on dividend @ 10% u/s 194 (if > Rs.5,000 to individual) — must be deducted and deposited.

---

### 7. MGT-14 Filing Checklist

Resolutions requiring MGT-14 filing within 30 days:
- [ ] Ordinary resolutions: Appointment/re-appointment of MD/WTD (S.196), Auditor appointment (S.139)
- [ ] Special resolutions: Buy-back (S.68), change of name (S.13), alteration of MOA/AOA, issue of shares on preferential basis (S.62), loans to directors (S.185 special cases), related party transactions if exceeding threshold
