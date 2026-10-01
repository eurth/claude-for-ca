"""Deterministic bank-statement line extract when the LLM does not return JSON."""

from __future__ import annotations

import re
from typing import Any

AMOUNT = r"[\d,]+\.\d{2}"
LINE = re.compile(rf"^(?P<date>\d{{2}}-\d{{2}}-\d{{4}})\s+(?P<narration>.+?)\s+(?P<a1>{AMOUNT})(?:\s+(?P<a2>{AMOUNT}))?\s*$")


def _num(raw: str) -> float:
    return float(raw.replace(",", ""))


def _category(narration: str) -> str:
    n = narration.upper()
    if "GST" in n or "GSTR" in n:
        return "GST"
    if "TDS" in n:
        return "TDS"
    if "SALARY" in n:
        return "salary"
    if "EMI" in n or "LOAN" in n:
        return "loan"
    if "INT/" in n or "INTEREST" in n:
        return "receipt"
    if "CASH" in n:
        return "unknown"
    if "UNKNOWN" in n:
        return "unknown"
    if any(tag in n for tag in ("NEFT", "RTGS", "IMPS", "UPI")) and not any(
        tag in n for tag in ("PMT", "RENT", "ELECTRIC")
    ):
        return "receipt" if "SALES" in n else "vendor payment"
    if "RENT" in n or "ELECTRIC" in n or "CHARGES" in n:
        return "vendor payment"
    return "unknown"


def parse_bank_statement(text: str) -> dict[str, Any]:
    opening = None
    closing = None
    om = re.search(rf"Opening balance:\s*({AMOUNT})", text, re.I)
    if om:
        opening = _num(om.group(1))
    cm = re.search(rf"Closing balance:\s*({AMOUNT})", text, re.I)
    if cm:
        closing = _num(cm.group(1))

    rows: list[dict[str, Any]] = []
    running = opening
    for raw in text.splitlines():
        match = LINE.match(raw.strip())
        if not match:
            continue
        amount = _num(match.group("a1"))
        balance = _num(match.group("a2")) if match.group("a2") else None
        if balance is None:
            balance = running
        debit = 0.0
        credit = 0.0
        if running is not None and balance is not None:
            if balance > running + 0.009:
                credit = amount
            else:
                debit = amount
            running = balance
        else:
            debit = amount
            running = balance
        narration = re.sub(r"\s+", " ", match.group("narration")).strip()
        rows.append(
            {
                "date": match.group("date"),
                "narration": narration,
                "debit": debit,
                "credit": credit,
                "balance": balance,
                "category": _category(narration),
            }
        )
    return {"rows": rows, "opening": opening, "closing": closing}
