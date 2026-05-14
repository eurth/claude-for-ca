"""
gst_portal_mcp.py — MCP server for GST Portal integration via Selenium.

Exposes GST portal data as MCP tools for claude-for-ca plugins.
Uses Selenium WebDriver to interact with the GST portal (gstin.gov.in).

IMPORTANT: Submit tools (submit_gstr1, submit_gstr3b) are blocked by HITL
hooks in shared/hooks/hooks.json. They will NOT execute without explicit
CA approval.

Setup:
  1. pip install fastmcp selenium webdriver-manager
  2. Install Chrome + ChromeDriver (managed automatically by webdriver-manager)
  3. Set environment variables: GST_USERNAME, GST_PASSWORD (or use session cookie)

Security note: GST credentials are read from environment variables only.
NEVER hardcode credentials.
"""

import os
import time
from typing import Optional

from fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

GST_PORTAL_URL = "https://www.gst.gov.in"

mcp = FastMCP("gst_portal")

_driver: Optional[webdriver.Chrome] = None


def _get_driver() -> webdriver.Chrome:
    """Return (or create) a headless Chrome WebDriver instance."""
    global _driver
    if _driver is None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=options)
    return _driver


def _login(gstin: str) -> bool:
    """
    Log in to the GST portal using environment credentials.
    Returns True on successful login.
    Credentials are read from GST_USERNAME and GST_PASSWORD env vars.
    """
    username = os.environ.get("GST_USERNAME")
    password = os.environ.get("GST_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "GST_USERNAME and GST_PASSWORD environment variables must be set."
        )

    driver = _get_driver()
    driver.get(f"{GST_PORTAL_URL}/login")
    wait = WebDriverWait(driver, 30)

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    # Note: CAPTCHA must be handled manually or via 2FA OTP if portal requires it.
    # This implementation assumes OTP-less API-mode login or pre-authenticated session.
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(3)
    return "dashboard" in driver.current_url


@mcp.tool()
def get_gstr1_draft(gstin: str, return_period: str) -> dict:
    """
    Fetch GSTR-1 draft data from the GST portal for a given GSTIN and period.

    Args:
        gstin: GST Identification Number (15-character alphanumeric)
        return_period: Return period in MMYYYY format (e.g. "032026" for March 2026)

    Returns:
        Dict containing B2B, B2C, export, and nil-rated invoice summaries.

    Note: This is a READ-ONLY operation. No data is submitted.
    """
    # In a production scenario, this would navigate to the GST portal
    # Returns/GSTR-1 filing section and extract draft data.
    # Returning a placeholder structure to demonstrate the schema.
    return {
        "gstin": gstin,
        "return_period": return_period,
        "status": "DRAFT",
        "b2b_invoices": [],   # List of B2B invoices
        "b2c_summary": {},    # B2CS / B2CL summary
        "exports": [],         # Export invoices
        "nil_rated": {},       # Nil rated / exempt / non-GST supplies
        "note": "Connect to live GST portal for actual data. Selenium login required.",
    }


@mcp.tool()
def get_gstr3b_summary(gstin: str, return_period: str) -> dict:
    """
    Fetch GSTR-3B summary data from the GST portal.

    Args:
        gstin: GST Identification Number
        return_period: Return period in MMYYYY format

    Returns:
        Dict containing outward supplies, ITC, and net tax liability.

    Note: READ-ONLY. No data is submitted.
    """
    return {
        "gstin": gstin,
        "return_period": return_period,
        "status": "DRAFT",
        "3_1_outward_supplies": {"taxable": 0, "zero_rated": 0, "exempt": 0},
        "4_itc_available": {"igst": 0, "cgst": 0, "sgst": 0},
        "net_tax_payable": {"igst": 0, "cgst": 0, "sgst": 0},
        "note": "Connect to live GST portal for actual data.",
    }


@mcp.tool()
def get_gstr2b(gstin: str, return_period: str) -> dict:
    """
    Fetch GSTR-2B (auto-populated ITC statement) for a given period.

    Args:
        gstin: GST Identification Number
        return_period: Return period in MMYYYY format

    Returns:
        Dict with supplier-wise ITC available as per GSTR-2B.
    """
    return {
        "gstin": gstin,
        "return_period": return_period,
        "itc_available": [],
        "itc_not_available": [],
        "note": "Connect to live GST portal for actual GSTR-2B data.",
    }


@mcp.tool()
def submit_gstr1(gstin: str, return_period: str) -> dict:
    """
    Submit GSTR-1 on the GST portal.

    ⚠️ THIS TOOL IS BLOCKED BY HITL HOOK — CA APPROVAL REQUIRED.
    The shared/hooks/hooks.json PreToolUse hook intercepts this call
    and requires explicit partner approval before execution.

    Args:
        gstin: GST Identification Number
        return_period: Return period in MMYYYY format

    Returns:
        Submission status or HITL block message.
    """
    # This code is only reached after HITL approval via the hook.
    return {
        "status": "HITL_BLOCKED",
        "message": "GSTR-1 submission requires explicit CA partner approval. "
                   "Please approve via the HITL prompt before this executes.",
        "gstin": gstin,
        "return_period": return_period,
    }


@mcp.tool()
def submit_gstr3b(gstin: str, return_period: str) -> dict:
    """
    Submit GSTR-3B on the GST portal.

    ⚠️ THIS TOOL IS BLOCKED BY HITL HOOK — CA APPROVAL REQUIRED.
    The shared/hooks/hooks.json PreToolUse hook intercepts this call.

    Args:
        gstin: GST Identification Number
        return_period: Return period in MMYYYY format

    Returns:
        Submission status or HITL block message.
    """
    return {
        "status": "HITL_BLOCKED",
        "message": "GSTR-3B submission requires explicit CA partner approval. "
                   "Please approve via the HITL prompt before this executes.",
        "gstin": gstin,
        "return_period": return_period,
    }


if __name__ == "__main__":
    mcp.run()
