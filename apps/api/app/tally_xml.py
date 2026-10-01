"""Tally voucher XML from a purchase register (v1 download-only)."""

from datetime import datetime
from xml.sax.saxutils import escape


def _amt(v) -> str:
    try:
        return f"{float(v):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def purchase_register_to_xml(rows: list[dict], company: str, date_str: str | None = None) -> str:
    vouchers = []
    for i, row in enumerate(rows, start=1):
        inv_date = (row.get("date") or row.get("invoice_date") or date_str or datetime.now().strftime("%Y%m%d")).replace("-", "")
        if len(inv_date) > 8:
            inv_date = inv_date[:8]
        party = escape(str(row.get("vendor") or row.get("vendor_name") or "Sundry Creditor"))
        inv = escape(str(row.get("invoice_no") or row.get("invoice_number") or i))
        taxable = _amt(row.get("taxable_value") or row.get("taxable"))
        cgst = _amt(row.get("cgst") or 0)
        sgst = _amt(row.get("sgst") or 0)
        igst = _amt(row.get("igst") or 0)
        total = _amt(row.get("total") or 0)
        gstin = escape(str(row.get("gstin") or ""))
        ledger = escape(str(row.get("ledger_head") or "Purchase A/c"))

        lines = [
            f'<LEDGERENTRY><LEDGERNAME>{ledger}</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><AMOUNT>-{taxable}</AMOUNT></LEDGERENTRY>'
        ]
        if float(cgst) > 0:
            lines.append(
                f'<LEDGERENTRY><LEDGERNAME>CGST Input</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><AMOUNT>-{cgst}</AMOUNT></LEDGERENTRY>'
            )
        if float(sgst) > 0:
            lines.append(
                f'<LEDGERENTRY><LEDGERNAME>SGST Input</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><AMOUNT>-{sgst}</AMOUNT></LEDGERENTRY>'
            )
        if float(igst) > 0:
            lines.append(
                f'<LEDGERENTRY><LEDGERNAME>IGST Input</LEDGERNAME><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><AMOUNT>-{igst}</AMOUNT></LEDGERENTRY>'
            )
        lines.append(
            f'<LEDGERENTRY><LEDGERNAME>{party}</LEDGERNAME><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE><AMOUNT>{total}</AMOUNT></LEDGERENTRY>'
        )
        vouchers.append(
            f"""<TALLYMESSAGE>
<VOUCHER VCHTYPE="Purchase" ACTION="Create">
<DATE>{inv_date}</DATE>
<VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
<VOUCHERNUMBER>{inv}</VOUCHERNUMBER>
<PARTYLEDGERNAME>{party}</PARTYLEDGERNAME>
<NARRATION>GSTIN {gstin} Invoice {inv}</NARRATION>
{''.join(lines)}
</VOUCHER>
</TALLYMESSAGE>"""
        )

    company_esc = escape(company or "Company")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ENVELOPE>
<HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER>
<BODY>
<IMPORTDATA>
<REQUESTDESC>
<REPORTNAME>Vouchers</REPORTNAME>
<STATICVARIABLES><SVCURRENTCOMPANY>{company_esc}</SVCURRENTCOMPANY></STATICVARIABLES>
</REQUESTDESC>
<REQUESTDATA>
{''.join(vouchers)}
</REQUESTDATA>
</IMPORTDATA>
</BODY>
</ENVELOPE>
"""
