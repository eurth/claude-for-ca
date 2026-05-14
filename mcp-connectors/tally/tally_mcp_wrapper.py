"""
tally_mcp_wrapper.py — MCP server for Tally ERP integration.

Exposes Tally data as MCP tools consumed by claude-for-ca plugins.
Uses Tally's built-in XML HTTP server (port 9000 by default).

Setup:
  1. Enable Tally HTTP server: Gateway of Tally → F12 Config → Advanced Config
     → Enable ODBC/HTTP Server → Port 9000
  2. pip install fastmcp requests lxml

Usage:
  python tally_mcp_wrapper.py
  Registers as MCP server named "tally" (matches .mcp.json in plugins).
"""

import xml.etree.ElementTree as ET
from typing import Optional
import requests
import os

from fastmcp import FastMCP

TALLY_URL = os.environ.get("TALLY_URL", "http://localhost:9000")

mcp = FastMCP("tally")


def _tally_post(xml_request: str) -> ET.Element:
    """POST an XML request to the Tally HTTP server and return the root element."""
    response = requests.post(
        TALLY_URL,
        data=xml_request.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        timeout=30,
    )
    response.raise_for_status()
    return ET.fromstring(response.text)


@mcp.tool()
def get_trial_balance(company_name: str, from_date: str, to_date: str) -> dict:
    """
    Fetch Trial Balance from Tally for the specified company and date range.

    Args:
        company_name: Tally company name (as configured in Tally)
        from_date: Start date in DD-MMM-YYYY format (e.g. 01-Apr-2025)
        to_date: End date in DD-MMM-YYYY format (e.g. 31-Mar-2026)

    Returns:
        Dict with ledger-wise debit/credit balances.
    """
    xml_req = f"""
    <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <EXPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Trial Balance</REPORTNAME>
            <STATICVARIABLES>
              <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
              <SVFROMDATE>{from_date}</SVFROMDATE>
              <SVTODATE>{to_date}</SVTODATE>
              <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
            </STATICVARIABLES>
          </REQUESTDESC>
        </EXPORTDATA>
      </BODY>
    </ENVELOPE>
    """
    root = _tally_post(xml_req)
    ledgers = []
    for ledger in root.iter("LEDGER"):
        name = ledger.findtext("NAME", "")
        closing = ledger.findtext("CLOSINGBALANCE", "0")
        ledgers.append({"ledger": name, "closing_balance": closing})
    return {"trial_balance": ledgers, "from": from_date, "to": to_date}


@mcp.tool()
def get_ledger_report(
    company_name: str, ledger_name: str, from_date: str, to_date: str
) -> dict:
    """
    Fetch ledger-wise transaction details from Tally.

    Args:
        company_name: Tally company name
        ledger_name: Exact ledger name as in Tally (e.g. "Output GST 18%")
        from_date: Start date DD-MMM-YYYY
        to_date: End date DD-MMM-YYYY

    Returns:
        Dict with list of vouchers for the ledger.
    """
    xml_req = f"""
    <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <EXPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Ledger</REPORTNAME>
            <STATICVARIABLES>
              <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
              <SVFROMDATE>{from_date}</SVFROMDATE>
              <SVTODATE>{to_date}</SVTODATE>
              <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
              <LEDGERNAME>{ledger_name}</LEDGERNAME>
            </STATICVARIABLES>
          </REQUESTDESC>
        </EXPORTDATA>
      </BODY>
    </ENVELOPE>
    """
    root = _tally_post(xml_req)
    vouchers = []
    for v in root.iter("VOUCHER"):
        vouchers.append(
            {
                "date": v.findtext("DATE", ""),
                "voucher_type": v.findtext("VOUCHERTYPENAME", ""),
                "narration": v.findtext("NARRATION", ""),
                "amount": v.findtext("AMOUNT", "0"),
            }
        )
    return {"ledger": ledger_name, "vouchers": vouchers}


@mcp.tool()
def get_balance_sheet(
    company_name: str, as_at_date: str
) -> dict:
    """
    Fetch Balance Sheet from Tally as at a given date.

    Args:
        company_name: Tally company name
        as_at_date: Date in DD-MMM-YYYY format

    Returns:
        Dict with assets and liabilities summary.
    """
    xml_req = f"""
    <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <EXPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Balance Sheet</REPORTNAME>
            <STATICVARIABLES>
              <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
              <SVTODATE>{as_at_date}</SVTODATE>
              <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
            </STATICVARIABLES>
          </REQUESTDESC>
        </EXPORTDATA>
      </BODY>
    </ENVELOPE>
    """
    root = _tally_post(xml_req)
    groups = []
    for g in root.iter("GROUP"):
        groups.append(
            {
                "name": g.findtext("NAME", ""),
                "closing_balance": g.findtext("CLOSINGBALANCE", "0"),
            }
        )
    return {"balance_sheet": groups, "as_at": as_at_date}


@mcp.tool()
def get_stock_report(
    company_name: str, from_date: str, to_date: str, stock_item: Optional[str] = None
) -> dict:
    """
    Fetch stock summary or stock item detail from Tally.

    Args:
        company_name: Tally company name
        from_date: Start date DD-MMM-YYYY
        to_date: End date DD-MMM-YYYY
        stock_item: Optional specific stock item name. If None, returns all items.

    Returns:
        List of stock items with opening, receipts, issued, closing quantities and values.
    """
    filter_xml = (
        f"<STOCKITEMNAME>{stock_item}</STOCKITEMNAME>" if stock_item else ""
    )
    xml_req = f"""
    <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <EXPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Stock Summary</REPORTNAME>
            <STATICVARIABLES>
              <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
              <SVFROMDATE>{from_date}</SVFROMDATE>
              <SVTODATE>{to_date}</SVTODATE>
              <SVCURRENTCOMPANY>{company_name}</SVCURRENTCOMPANY>
              {filter_xml}
            </STATICVARIABLES>
          </REQUESTDESC>
        </EXPORTDATA>
      </BODY>
    </ENVELOPE>
    """
    root = _tally_post(xml_req)
    items = []
    for item in root.iter("STOCKITEM"):
        items.append(
            {
                "name": item.findtext("NAME", ""),
                "closing_qty": item.findtext("CLOSINGQTY", "0"),
                "closing_value": item.findtext("CLOSINGVALUE", "0"),
            }
        )
    return {"stock_items": items}


@mcp.tool()
def create_voucher(
    company_name: str,
    voucher_type: str,
    date: str,
    narration: str,
    debit_ledger: str,
    credit_ledger: str,
    amount: float,
) -> dict:
    """
    Create a voucher in Tally. REQUIRES HUMAN APPROVAL before posting.
    This tool is blocked by a HITL hook — the CA must approve before this executes.

    Args:
        company_name: Tally company name
        voucher_type: e.g. "Journal", "Payment", "Receipt", "Purchase", "Sales"
        date: Date in DD-MMM-YYYY format
        narration: Voucher narration / description
        debit_ledger: Ledger to debit
        credit_ledger: Ledger to credit
        amount: Amount in Rs. (positive number)

    Returns:
        Success/failure dict from Tally.
    """
    xml_req = f"""
    <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
      </HEADER>
      <BODY>
        <IMPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Vouchers</REPORTNAME>
          </REQUESTDESC>
          <REQUESTDATA>
            <TALLYMESSAGE xmlns:UDF="TallyUDF">
              <VOUCHER VCHTYPE="{voucher_type}" ACTION="Create">
                <DATE>{date}</DATE>
                <NARRATION>{narration}</NARRATION>
                <VOUCHERTYPENAME>{voucher_type}</VOUCHERTYPENAME>
                <ALLLEDGERENTRIES.LIST>
                  <LEDGERNAME>{debit_ledger}</LEDGERNAME>
                  <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                  <AMOUNT>-{amount}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
                <ALLLEDGERENTRIES.LIST>
                  <LEDGERNAME>{credit_ledger}</LEDGERNAME>
                  <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                  <AMOUNT>{amount}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
              </VOUCHER>
            </TALLYMESSAGE>
          </REQUESTDATA>
        </IMPORTDATA>
      </BODY>
    </ENVELOPE>
    """
    root = _tally_post(xml_req)
    status = root.findtext(".//STATUS", "Unknown")
    return {"status": status, "voucher_type": voucher_type, "amount": amount, "date": date}


if __name__ == "__main__":
    mcp.run()
