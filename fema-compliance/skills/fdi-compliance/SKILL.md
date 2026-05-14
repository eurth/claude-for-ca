---
name: fdi-compliance
description: >
  FDI inflow compliance under FEMA — FC-GPR (equity allotment to foreigners),
  FC-TRS (transfer of shares), and FIFP (downstream investment). Covers RBI
  reporting, pricing norms (FEMA 20R), sectoral caps, approval route vs automatic
  route, and deferred consideration requirements.
when_to_use: >
  When a company receives FDI (foreign equity investment), allots shares to a
  foreign investor, or when shares are transferred between a resident and non-resident.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# FDI Compliance — FC-GPR / FC-TRS

**FINANCIAL INTEGRITY**: FEMA violations attract compounding penalties. Late filing of FC-GPR/FC-TRS is compoundable but time-sensitive. Any FDI in restricted sectors requires prior government approval. All pricing of shares must comply with FEMA 20R valuation norms — do not conclude without CA/SEBI-registered valuer certificate.

## FDI Routes

| Route | Applicable Sectors | Approval Required |
|---|---|---|
| Automatic Route | Most sectors — up to sectoral cap | No prior RBI/Government approval |
| Government Route | Defense, media, telecom (some), retail, financial services etc. | Prior FIPB/DPIIT/Sectoral Ministry approval |

**Always check the current FDI Policy** (DPIIT website) for latest sectoral caps before advising.

## FC-GPR — Fresh Issue of Shares to Foreigner

**Trigger**: Indian company allots equity/preference shares/convertible debentures to a non-resident.

**Timeline**: Report to RBI via FC-GPR within **30 days** of allotment of shares.

**How to file**: Through FIRMS portal (Foreign Investment Reporting and Management System) on RBI's website.

**Information required**:
- Company CIN + PAN + Industry
- Foreign investor name, country, investment route (FDI/NRI/etc.)
- Number of shares allotted + face value + premium + total consideration received
- Date of inflow + Bank reference number (FIRC / e-FIRC from the bank)
- Valuation certificate (as per FEMA 20R): For unlisted companies — DCF method by SEBI-registered valuer or CA (based on internationally accepted pricing methodology)
- KYC of foreign investor

**Pricing Norms (FEMA 20R)**:
- Unlisted companies: Not less than FMV (DCF or NAV — as per internationally accepted pricing methodology)
- Listed companies: Not less than SEBI ICDR pricing norms (market price based formula)

```
FC-GPR CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Investment in permitted sector (check FDI policy)
[ ] Within sectoral cap
[ ] Inward remittance received via banking channel (FIRC obtained)
[ ] Valuation certificate by registered valuer (for unlisted)
[ ] Board resolution for allotment passed
[ ] Form PAS-3 filed with MCA
[ ] FC-GPR filed within 30 days of allotment
[ ] Share certificate issued to foreign investor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## FC-TRS — Transfer of Shares Between Resident and Non-Resident

**Trigger**: Transfer of equity shares from a resident to a non-resident (or vice versa).

**Timeline**: Report within 60 days of receipt/remittance of consideration.

**Pricing Norms for Transfer (FEMA 20R)**:
- Resident to Non-Resident: Transfer at not LESS than FMV (floor price)
- Non-Resident to Resident: Transfer at not MORE than FMV (ceiling price)
- Listed companies: SEBI norms apply

```
FC-TRS CHECKLIST:
[ ] Valuation certificate obtained (for unlisted — DCF/NAV)
[ ] Consideration received/paid within 60 days of transfer
[ ] FC-TRS reported on FIRMS portal within 60 days
[ ] Share transfer deed executed + stamp duty paid
[ ] Form SH-4 / private agreement as applicable
[ ] New holder registered in company's share register
```

## Annual Return (FLA)

All companies with FDI or ODI must file:
- **FLA (Foreign Liabilities and Assets) return** — due by **15 July** each year
- Filed with RBI: flair.rbi.org.in
- Covers all FDI received, ODI made, and outstanding FLA position as at 31 March
