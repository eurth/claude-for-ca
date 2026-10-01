import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
(ROOT / "data").mkdir(parents=True, exist_ok=True)
os.environ["DATABASE_URL"] = f"sqlite:///{(ROOT / 'data' / 'test.db').as_posix()}"
os.environ["PACKS_DIR"] = str(ROOT / "packs")
os.environ["JWT_SECRET"] = "test-secret"
os.environ["LLM_PROVIDER"] = "mock"
sys.path.insert(0, str(ROOT / "apps" / "api"))

from fastapi.testclient import TestClient
from app.db import Base, engine
from app.main import app

Base.metadata.drop_all(bind=engine)


def _login(client, email="partner@gorantla.local"):
    login = client.post("/api/auth/login", json={"email": email, "password": "changeme"})
    assert login.status_code == 200, login.text
    token = login.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def _entity_and_gstins(client, headers):
    clients = client.get("/api/clients", headers=headers).json()
    entity = clients["entities"][0]
    gstins = [r for r in entity["registrations"] if r["kind"] == "gstin"]
    return entity, gstins


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["ok"] is True


def test_login_and_gstr3b_run_creates_approval():
    with TestClient(app) as client:
        h = _login(client)
        entity, gstins = _entity_and_gstins(client, h)
        gstin = next(r for r in gstins if r["value"].startswith("37"))
        created = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "gstr3b-review",
                "entity_id": entity["id"],
                "registration_id": gstin["id"],
                "period": "2026-04",
            },
        )
        assert created.status_code == 200, created.text
        pack_id = created.json()["id"]
        ran = client.post(f"/api/workpacks/{pack_id}/run", headers=h)
        assert ran.status_code == 200, ran.text
        body = ran.json()
        assert body["status"] == "pending_approval"
        inbox = client.get("/api/approvals", headers=h).json()
        assert any(a["workpack_id"] == pack_id for a in inbox["approvals"])


def test_discover_suggests_a_feature():
    with TestClient(app) as client:
        h = _login(client, "intern@gorantla.local")
        entity, _ = _entity_and_gstins(client, h)
        created = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "discover",
                "entity_id": entity["id"],
                "note": "I need to extract purchase invoices from PDFs",
            },
        )
        pack_id = created.json()["id"]
        ran = client.post(f"/api/workpacks/{pack_id}/run", headers=h)
        assert ran.status_code == 200, ran.text
        types = [a["type"] for a in ran.json()["artifacts"]]
        assert "router_suggestion" in types


def test_pilot_invoice_bank_notice_and_tally():
    with TestClient(app) as client:
        h = _login(client)
        entity, gstins = _entity_and_gstins(client, h)
        gstin = next(r for r in gstins if r["value"].startswith("37"))

        inv = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "pdf-data-extractor",
                "entity_id": entity["id"],
                "registration_id": gstin["id"],
                "period": "2026-06",
            },
        )
        inv_id = inv.json()["id"]
        inv_ran = client.post(f"/api/workpacks/{inv_id}/run", headers=h).json()
        assert "purchase_register" in [a["type"] for a in inv_ran["artifacts"]]

        bank = client.post(
            "/api/workpacks",
            headers=h,
            json={"feature_id": "bank-statement-processor", "entity_id": entity["id"], "period": "2026-06"},
        )
        bank_ran = client.post(f"/api/workpacks/{bank.json()['id']}/run", headers=h).json()
        assert "bank_ledger" in [a["type"] for a in bank_ran["artifacts"]]

        notice = client.post(
            "/api/workpacks",
            headers=h,
            json={"feature_id": "notice-triage", "entity_id": entity["id"]},
        )
        notice_ran = client.post(f"/api/workpacks/{notice.json()['id']}/run", headers=h).json()
        types = [a["type"] for a in notice_ran["artifacts"]]
        assert "draft_reply" in types
        assert notice_ran["status"] == "pending_approval"

        tally = client.post(
            "/api/workpacks",
            headers=h,
            json={"feature_id": "tally-import-builder", "entity_id": entity["id"], "period": "2026-06"},
        )
        tally_id = tally.json()["id"]
        tally_ran = client.post(f"/api/workpacks/{tally_id}/run", headers=h).json()
        assert tally_ran["status"] == "pending_approval"
        xml = next(a for a in tally_ran["artifacts"] if a["type"] == "tally_xml")
        blocked = client.get(f"/api/workpacks/{tally_id}/files/{xml['id']}", headers=h)
        assert blocked.status_code == 403

        inbox = client.get("/api/approvals", headers=h).json()
        approval = next(a for a in inbox["approvals"] if a["workpack_id"] == tally_id)
        decided = client.post(
            f"/api/approvals/{approval['id']}",
            headers=h,
            json={"decision": "approve"},
        )
        assert decided.status_code == 200
        allowed = client.get(f"/api/workpacks/{tally_id}/files/{xml['id']}", headers=h)
        assert allowed.status_code == 200
        assert b"<ENVELOPE>" in allowed.content or b"TALLY" in allowed.content.upper() or b"LEDGER" in allowed.content.upper()


def test_artifact_reuse_same_gstin_not_other():
    with TestClient(app) as client:
        h = _login(client)
        entity, gstins = _entity_and_gstins(client, h)
        ap = next(r for r in gstins if r["value"].startswith("37"))
        ka = next(r for r in gstins if r["value"].startswith("29"))

        inv = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "pdf-data-extractor",
                "entity_id": entity["id"],
                "registration_id": ap["id"],
                "period": "2026-07",
            },
        )
        client.post(f"/api/workpacks/{inv.json()['id']}/run", headers=h)

        same = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "gstr3b-review",
                "entity_id": entity["id"],
                "registration_id": ap["id"],
                "period": "2026-07",
            },
        )
        same_ran = client.post(f"/api/workpacks/{same.json()['id']}/run", headers=h).json()
        reused = next((a for a in same_ran["artifacts"] if a["type"] == "reused_context"), None)
        assert reused is not None
        assert "purchase_register" in reused["json"]["types"]

        other = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "gstr3b-review",
                "entity_id": entity["id"],
                "registration_id": ka["id"],
                "period": "2026-07",
            },
        )
        other_ran = client.post(f"/api/workpacks/{other.json()['id']}/run", headers=h).json()
        other_reused = next((a for a in other_ran["artifacts"] if a["type"] == "reused_context"), None)
        types = (other_reused or {"json": {"types": []}})["json"]["types"]
        assert "purchase_register" not in types


def test_intern_cannot_approve():
    with TestClient(app) as client:
        partner = _login(client)
        intern = _login(client, "intern@gorantla.local")
        entity, gstins = _entity_and_gstins(client, partner)
        gstin = next(r for r in gstins if r["value"].startswith("37"))
        created = client.post(
            "/api/workpacks",
            headers=partner,
            json={
                "feature_id": "gstr3b-review",
                "entity_id": entity["id"],
                "registration_id": gstin["id"],
                "period": "2026-08",
            },
        )
        pack_id = created.json()["id"]
        client.post(f"/api/workpacks/{pack_id}/run", headers=partner)
        inbox = client.get("/api/approvals", headers=partner).json()
        approval = next(a for a in inbox["approvals"] if a["workpack_id"] == pack_id)
        denied = client.post(
            f"/api/approvals/{approval['id']}",
            headers=intern,
            json={"decision": "approve"},
        )
        assert denied.status_code == 403
        intern_inbox = client.get("/api/approvals", headers=intern)
        assert intern_inbox.status_code == 403


def test_invoice_pdf_extracts_and_replaces_on_rerun():
    with TestClient(app) as client:
        h = _login(client)
        entity, gstins = _entity_and_gstins(client, h)
        gstin = next(r for r in gstins if r["value"].startswith("37"))
        created = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "pdf-data-extractor",
                "entity_id": entity["id"],
                "registration_id": gstin["id"],
                "period": "2026-04",
            },
        )
        pack_id = created.json()["id"]
        samples = ROOT / "Test" / "samples" / "invoices"
        for name in ("INV-ST-1042-Sharma-Traders.pdf", "INV-ST-1042-duplicate.pdf"):
            with (samples / name).open("rb") as fh:
                up = client.post(
                    f"/api/workpacks/{pack_id}/files",
                    headers=h,
                    files={"upload": (name, fh, "application/pdf")},
                    data={"artifact_type": "purchase_invoice"},
                )
                assert up.status_code == 200, up.text
        ran = client.post(f"/api/workpacks/{pack_id}/run", headers=h)
        assert ran.status_code == 200, ran.text
        body = ran.json()
        registers = [a for a in body["artifacts"] if a["type"] == "purchase_register"]
        assert len(registers) == 1
        rows = registers[0]["json"]["rows"]
        assert any(r["invoice_no"] == "ST/1042" for r in rows)
        exceptions = next(a for a in body["artifacts"] if a["type"] == "exception_report")
        assert any("Duplicate" in item for item in exceptions["json"]["items"])
        again = client.post(f"/api/workpacks/{pack_id}/run", headers=h).json()
        assert len([a for a in again["artifacts"] if a["type"] == "purchase_register"]) == 1
        assert len([a for a in again["artifacts"] if a["is_input"]]) == 2


def test_master_accounts_and_excel_download():
    with TestClient(app) as client:
        h = _login(client)
        entity, gstins = _entity_and_gstins(client, h)
        gstin = next(r for r in gstins if r["value"].startswith("37"))
        inv = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "pdf-data-extractor",
                "entity_id": entity["id"],
                "registration_id": gstin["id"],
                "period": "2026-04",
            },
        )
        pack_id = inv.json()["id"]
        sample = ROOT / "Test" / "samples" / "invoices" / "INV-ST-1042-Sharma-Traders.pdf"
        with sample.open("rb") as fh:
            client.post(
                f"/api/workpacks/{pack_id}/files",
                headers=h,
                files={"upload": (sample.name, fh, "application/pdf")},
                data={"artifact_type": "purchase_invoice"},
            )
        client.post(f"/api/workpacks/{pack_id}/run", headers=h)
        master = client.post(
            "/api/workpacks",
            headers=h,
            json={
                "feature_id": "master-accounts-sheet",
                "entity_id": entity["id"],
                "period": "2026-04",
            },
        )
        ran = client.post(f"/api/workpacks/{master.json()['id']}/run", headers=h)
        assert ran.status_code == 200, ran.text
        body = ran.json()
        xlsx = next(a for a in body["artifacts"] if a["type"] == "master_accounts_xlsx")
        dl = client.get(f"/api/workpacks/{master.json()['id']}/files/{xlsx['id']}", headers=h)
        assert dl.status_code == 200
        assert dl.content[:2] == b"PK"
        feats = client.get("/api/features", headers=h).json()["features"]
        assert len(feats) >= 45
        assert any(f["id"] == "itc-reconcile" for f in feats)

