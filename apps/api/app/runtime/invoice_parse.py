"""Extract GST tax-invoice fields from PDF text when the LLM does not return rows."""

from __future__ import annotations

import re
from typing import Any

GSTIN_RE = re.compile(r"\b([0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][A-Z0-9]Z[A-Z0-9])\b", re.I)
INV_RE = re.compile(r"Invoice No:\s*(\S+)\s+Date:\s*(\S.+)$", re.I | re.M)
BUYER_RE = re.compile(r"Buyer GSTIN:\s*([0-9A-Z]{15})", re.I)
LINE_RE = re.compile(
    r"^(?P<hsn>\d{4,8})\s+(?P<desc>.+?)\s+(?P<qty>\d+)\s+"
    r"(?P<rate>[\d,]+\.\d{2})\s+(?P<taxable>[\d,]+\.\d{2})\s+"
    r"(?P<cgst>[\d,]+\.\d{2})\s+(?P<sgst>[\d,]+\.\d{2})\s+"
    r"(?P<igst>[\d,]+\.\d{2})\s+(?P<total>[\d,]+\.\d{2})\s*$"
)


def _num(raw: str) -> float:
    return float(raw.replace(",", ""))


def parse_invoice_text(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    inv = INV_RE.search(text)
    gstins = GSTIN_RE.findall(text)
    if not inv or not gstins:
        return None
    vendor_gstin = gstins[0].upper()
    buyer_m = BUYER_RE.search(text)
    buyer_gstin = (buyer_m.group(1) if buyer_m else (gstins[1] if len(gstins) > 1 else "")).upper()
    vendor = "Unknown vendor"
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.upper().startswith("TAX INVOICE"):
            continue
        if "test document" in stripped.lower():
            continue
        if stripped.upper().startswith("GSTIN"):
            break
        vendor = stripped
        break
    rows = []
    for line in text.splitlines():
        match = LINE_RE.match(line.strip())
        if not match:
            continue
        rows.append(
            {
                "vendor": vendor,
                "gstin": vendor_gstin,
                "invoice_no": inv.group(1).strip(),
                "date": inv.group(2).strip(),
                "buyer_gstin": buyer_gstin,
                "hsn": match.group("hsn"),
                "description": re.sub(r"\s+", " ", match.group("desc")).strip(),
                "qty": int(match.group("qty")),
                "taxable_value": _num(match.group("taxable")),
                "cgst": _num(match.group("cgst")),
                "sgst": _num(match.group("sgst")),
                "igst": _num(match.group("igst")),
                "total": _num(match.group("total")),
            }
        )
    if not rows:
        return None
    return {"rows": rows}


def exception_items(rows: list[dict[str, Any]], job_gstin: str | None = None) -> list[str]:
    items: list[str] = []
    seen: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (str(row.get("invoice_no") or ""), str(row.get("gstin") or ""))
        seen[key] = seen.get(key, 0) + 1
        taxable = float(row.get("taxable_value") or 0)
        cgst = float(row.get("cgst") or 0)
        sgst = float(row.get("sgst") or 0)
        igst = float(row.get("igst") or 0)
        total = float(row.get("total") or 0)
        if abs(taxable + cgst + sgst + igst - total) > 1:
            items.append(f"{row.get('invoice_no')}: tax components do not add to invoice total.")
        vendor_st = str(row.get("gstin") or "")[:2]
        buyer_st = str(row.get("buyer_gstin") or job_gstin or "")[:2]
        if vendor_st and buyer_st and vendor_st != buyer_st and (cgst + sgst) > 0:
            items.append(f"{row.get('invoice_no')}: inter-state supply should use IGST, not CGST/SGST.")
        if vendor_st and buyer_st and vendor_st == buyer_st and igst > 0:
            items.append(f"{row.get('invoice_no')}: intra-state supply should not carry IGST.")
        if job_gstin and row.get("buyer_gstin") and row["buyer_gstin"].upper() != job_gstin.upper():
            items.append(
                f"{row.get('invoice_no')}: buyer GSTIN {row['buyer_gstin']} differs from this job's GSTIN {job_gstin}."
            )
    for (inv_no, gstin), count in seen.items():
        if count > 1 and inv_no:
            items.append(f"Duplicate invoice number {inv_no} ({gstin}).")
    return items


def parse_invoice_uploads(uploads: list[dict], job_gstin: str | None = None) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for upload in uploads:
        parsed = parse_invoice_text(upload.get("text_excerpt") or "")
        if parsed:
            rows.extend(parsed["rows"])
    return {"rows": rows, "items": exception_items(rows, job_gstin)}
