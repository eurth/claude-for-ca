"""
mca21_mcp.py — MCP server for MCA21 V3 API integration.

Exposes MCA21 (Ministry of Corporate Affairs) data as MCP tools for
claude-for-ca MCA secretarial plugin.

MCA21 V3 API portal: www.mca.gov.in/content/mca/global/en/data-and-reports/api.html

Setup:
  pip install fastmcp requests

Credentials: Set MCA_CLIENT_ID, MCA_CLIENT_SECRET env vars (from MCA portal API key).
"""

import os
from typing import Optional

import requests
from fastmcp import FastMCP

MCA_API_BASE = "https://api.mca.gov.in/v3"

mcp = FastMCP("mca21")

_access_token: Optional[str] = None


def _get_access_token() -> str:
    """
    Fetch OAuth2 access token from MCA21 API.
    Uses client_credentials grant with MCA_CLIENT_ID and MCA_CLIENT_SECRET.
    """
    global _access_token
    if _access_token:
        return _access_token

    client_id = os.environ.get("MCA_CLIENT_ID")
    client_secret = os.environ.get("MCA_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "MCA_CLIENT_ID and MCA_CLIENT_SECRET environment variables must be set."
        )

    response = requests.post(
        f"{MCA_API_BASE}/auth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    response.raise_for_status()
    _access_token = response.json()["access_token"]
    return _access_token


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {_get_access_token()}",
        "Content-Type": "application/json",
    }


@mcp.tool()
def get_company_profile(cin: str) -> dict:
    """
    Fetch company master data from MCA21 for a given CIN.

    Args:
        cin: Corporate Identification Number (21-character)
              e.g. "U72200KA2020PTC123456"

    Returns:
        Dict with company name, status, registered address, directors list,
        authorised capital, paid-up capital, date of incorporation.
    """
    response = requests.get(
        f"{MCA_API_BASE}/company/master/{cin}",
        headers=_headers(),
        timeout=30,
    )
    if response.status_code == 404:
        return {"error": f"Company with CIN {cin} not found in MCA21."}
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_director_details(din: str) -> dict:
    """
    Fetch director master data from MCA21 for a given DIN.

    Args:
        din: Director Identification Number (8-digit)

    Returns:
        Dict with director name, DOB, address, DIN approval date,
        list of companies associated.
    """
    response = requests.get(
        f"{MCA_API_BASE}/director/master/{din}",
        headers=_headers(),
        timeout=30,
    )
    if response.status_code == 404:
        return {"error": f"Director with DIN {din} not found."}
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_filing_status(cin: str, form_name: Optional[str] = None) -> dict:
    """
    Get filing status for a company's MCA forms.

    Args:
        cin: Corporate Identification Number
        form_name: Optional filter by form name (e.g. "AOC-4", "MGT-7").
                   If None, returns all recent filings.

    Returns:
        List of filings with form name, date of filing, SRN, and status.
    """
    params: dict = {"cin": cin}
    if form_name:
        params["formName"] = form_name

    response = requests.get(
        f"{MCA_API_BASE}/filings",
        headers=_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


@mcp.tool()
def file_mca_form(
    cin: str,
    form_name: str,
    form_data: dict,
    signed_pdf_path: str,
) -> dict:
    """
    File an MCA form on MCA21 V3 portal.

    ⚠️ THIS TOOL IS BLOCKED BY HITL HOOK — CA/CS APPROVAL REQUIRED.
    The shared/hooks/hooks.json PreToolUse hook intercepts this call.

    Args:
        cin: Corporate Identification Number
        form_name: Form to file (e.g. "AOC-4", "MGT-7", "ADT-1")
        form_data: Dict containing form field values
        signed_pdf_path: Path to the DSC-signed PDF of the form

    Returns:
        SRN (Service Request Number) and filing status, or HITL block message.
    """
    return {
        "status": "HITL_BLOCKED",
        "message": f"{form_name} filing requires explicit CA/CS partner approval. "
                   "Approve via HITL prompt before this executes.",
        "cin": cin,
        "form_name": form_name,
    }


if __name__ == "__main__":
    mcp.run()
