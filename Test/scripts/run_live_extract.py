"""Upload sample PDFs and run Extract invoices / bank statement against the live API."""

from __future__ import annotations

import json
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
TEST = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8000"


def main() -> None:
    login = httpx.post(
        f"{BASE}/api/auth/login",
        json={"email": "partner@gorantla.local", "password": "changeme"},
        timeout=30,
    )
    login.raise_for_status()
    token = login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    clients = httpx.get(f"{BASE}/api/clients", headers=headers, timeout=30).json()
    entity = clients["entities"][0]
    gstin = next(r for r in entity["registrations"] if r["value"].startswith("37"))

    inv = TEST / "samples" / "invoices" / "INV-ST-1042-Sharma-Traders.pdf"
    bank = TEST / "samples" / "bank" / "HDFC-50200011223344-Apr-2026.pdf"
    if not inv.exists() or not bank.exists():
        raise SystemExit("Run Test/scripts/generate_samples.py first")

    created = httpx.post(
        f"{BASE}/api/workpacks",
        headers=headers,
        json={
            "feature_id": "pdf-data-extractor",
            "entity_id": entity["id"],
            "registration_id": gstin["id"],
            "period": "2026-04",
        },
        timeout=30,
    )
    created.raise_for_status()
    pack_id = created.json()["id"]
    with inv.open("rb") as fh:
        up = httpx.post(
            f"{BASE}/api/workpacks/{pack_id}/files",
            headers=headers,
            files={"upload": (inv.name, fh, "application/pdf")},
            data={"artifact_type": "purchase_invoice"},
            timeout=60,
        )
        up.raise_for_status()
    ran = httpx.post(f"{BASE}/api/workpacks/{pack_id}/run", headers=headers, timeout=180)
    ran.raise_for_status()
    inv_body = ran.json()
    detail = httpx.get(f"{BASE}/api/workpacks/{pack_id}", headers=headers, timeout=30).json()

    def artifact_types(pack):
        return [a.get("type") for a in pack.get("artifacts") or []]

    def ledger_rows(pack):
        for art in pack.get("artifacts") or []:
            if art.get("type") == "bank_ledger":
                data = art.get("json") or art.get("data") or {}
                return len((data or {}).get("rows") or [])
        return 0

    bcreated = httpx.post(
        f"{BASE}/api/workpacks",
        headers=headers,
        json={"feature_id": "bank-statement-processor", "entity_id": entity["id"], "period": "2026-04"},
        timeout=30,
    )
    bcreated.raise_for_status()
    bid = bcreated.json()["id"]
    with bank.open("rb") as fh:
        httpx.post(
            f"{BASE}/api/workpacks/{bid}/files",
            headers=headers,
            files={"upload": (bank.name, fh, "application/pdf")},
            data={"artifact_type": "bank_pdf"},
            timeout=60,
        ).raise_for_status()
    bran = httpx.post(f"{BASE}/api/workpacks/{bid}/run", headers=headers, timeout=180)
    bran.raise_for_status()
    bank_body = bran.json()
    bdetail = httpx.get(f"{BASE}/api/workpacks/{bid}", headers=headers, timeout=30).json()

    out = {
        "invoice": {
            "pack_id": pack_id,
            "status": inv_body.get("status"),
            "summary": (inv_body.get("summary") or "")[:500],
            "artifacts": artifact_types(inv_body),
            "model_used": detail.get("model_used") or inv_body.get("model_used"),
        },
        "bank": {
            "pack_id": bid,
            "status": bank_body.get("status"),
            "summary": (bank_body.get("summary") or "")[:500],
            "artifacts": artifact_types(bank_body),
            "ledger_rows": ledger_rows(bank_body),
            "model_used": bdetail.get("model_used") or bank_body.get("model_used"),
        },
    }
    dest = TEST / "results" / "live_extract.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
