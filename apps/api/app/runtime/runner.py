import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.hitl import template_for
from app.models import (
    Approval,
    Artifact,
    AuditEvent,
    Firm,
    LegalEntity,
    Message,
    Notice,
    Registration,
    User,
    Workpack,
)
from app.runtime.bank_parse import parse_bank_statement
from app.runtime.catalog import get_feature
from app.runtime.gateway import complete
from app.runtime.invoice_parse import parse_invoice_uploads
from app.runtime.loader import load_skill
from app.tally_xml import purchase_register_to_xml
from app.workbook import bank_rows_table, build_master_accounts, purchase_rows_table, write_rows_xlsx

OUTPUT_INSTRUCTION = """
You are executing this job now against UPLOADED DOCUMENT TEXT. Do not restate these instructions.
Reusable artifacts are matching context only — never a substitute for extracting the uploaded file.
Always finish with a single JSON object in a ```json fence using this shape:
{
  "summary": "short staff-facing summary of what was extracted (no model names, no procedure recap)",
  "artifacts": [
    {"type": "purchase_register|sales_register|bank_ledger|exception_report|gstr3b_working|notice_summary|draft_reply|router_suggestion",
     "title": "human title",
     "data": {} }
  ],
  "suggested_feature_id": null,
  "approval": null
}
If FEATURE_ID is pdf-data-extractor, include purchase_register with data.rows from each invoice.
If FEATURE_ID is bank-statement-processor, include bank_ledger with data.rows (date, narration, debit, credit, balance, category) for every statement line, plus opening and closing.
Documents marked "test" or "sample" are still extractable — extract the figures.
Inter-state IGST (vendor GSTIN state ≠ buyer GSTIN state) is not an error.
Do not file any return or post to Tally. Draft only. Cite Indian law sections where relevant.
"""


def _pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)[:20000]
    except Exception:
        return ""


def reusable_artifacts(db: Session, pack: Workpack, consumes: list[str]) -> list[Artifact]:
    if not consumes:
        return []
    q = (
        db.query(Artifact)
        .filter(
            Artifact.firm_id == pack.firm_id,
            Artifact.entity_id == pack.entity_id,
            Artifact.artifact_type.in_(consumes),
            Artifact.is_input.is_(False),
            Artifact.workpack_id != pack.id,
        )
        .order_by(Artifact.created_at.desc())
    )
    if pack.registration_id:
        q = q.filter(
            (Artifact.registration_id == pack.registration_id) | (Artifact.registration_id.is_(None))
        )
    if pack.period:
        q = q.filter((Artifact.period == pack.period) | (Artifact.period.is_(None)))
    seen = set()
    out = []
    for art in q.all():
        if art.artifact_type in seen:
            continue
        seen.add(art.artifact_type)
        out.append(art)
    return out


def run_workpack(db: Session, pack: Workpack, user: User) -> Workpack:
    feature = get_feature(pack.feature_id)
    firm = db.get(Firm, pack.firm_id)
    entity = db.get(LegalEntity, pack.entity_id)
    registration = db.get(Registration, pack.registration_id) if pack.registration_id else None
    skill = load_skill(pack.feature_id)
    prior = reusable_artifacts(db, pack, feature.get("consumes") or [])

    context = {
        "firm": {"name": firm.name, "ca_name": firm.ca_name, "gstin": firm.gstin, "jurisdiction": firm.jurisdiction},
        "entity": {
            "name": entity.name,
            "pan": entity.pan,
            "cin": entity.cin,
            "tally_company": entity.tally_company,
            "entity_type": entity.entity_type,
        },
        "registration": None
        if not registration
        else {"kind": registration.kind, "value": registration.value, "state": registration.state, "cadence": registration.filing_cadence},
        "period": pack.period,
        "reusable_artifacts": [
            {"type": a.artifact_type, "title": a.title, "data": a.json_data} for a in prior
        ],
    }

    uploads = []
    for art in pack.artifacts:
        if art.is_input and art.path:
            p = Path(art.path)
            snippet = _pdf_text(p) if p.suffix.lower() == ".pdf" else ""
            uploads.append({"filename": p.name, "text_excerpt": snippet[:8000]})

    _reset_run_outputs(db, pack)

    messages = [
        {"role": "system", "content": skill + "\n\n" + OUTPUT_INSTRUCTION},
        {
            "role": "user",
            "content": f"FEATURE_ID: {pack.feature_id}\nPRACTICE CONTEXT (JSON):\n"
            + json.dumps(context, default=str)
            + "\n\nUPLOADED DOCUMENT TEXT:\n"
            + json.dumps(uploads, default=str),
        },
    ]
    for msg in pack.messages:
        messages.append({"role": msg.role, "content": msg.content})

    pack.status = "running"
    db.commit()

    parsed = None
    result_provider = "local"
    result_model = "parser"
    if pack.feature_id == "bank-statement-processor":
        excerpt = "\n".join(u.get("text_excerpt") or "" for u in uploads)
        ledger = parse_bank_statement(excerpt)
        if ledger.get("rows"):
            unknown = [r["narration"] for r in ledger["rows"] if r.get("category") == "unknown"]
            parsed = {
                "summary": (
                    f"Extracted {len(ledger['rows'])} bank rows. "
                    f"Opening {ledger.get('opening')}, closing {ledger.get('closing')}."
                ),
                "artifacts": [
                    {"type": "bank_ledger", "title": "Bank ledger", "data": ledger},
                    {"type": "exception_report", "title": "Exceptions", "data": {"items": unknown}},
                ],
            }
            result_model = "parser:bank_statement"
    elif pack.feature_id in ("pdf-data-extractor", "email-invoice-fetch"):
        job_gstin = registration.value if registration and registration.kind == "gstin" else None
        extracted = parse_invoice_uploads(uploads, job_gstin)
        if extracted.get("rows"):
            note = ""
            if pack.feature_id == "email-invoice-fetch":
                note = " Treated as email attachments (live Gmail is v2)."
            parsed = {
                "summary": f"Extracted {len(extracted['rows'])} invoice line(s) from the uploaded PDFs.{note}",
                "artifacts": [
                    {"type": "purchase_register", "title": "Purchase register", "data": {"rows": extracted["rows"]}},
                    {"type": "exception_report", "title": "Exceptions", "data": {"items": extracted["items"]}},
                ],
            }
            result_model = "parser:invoice"
    elif pack.feature_id == "master-accounts-sheet":
        purchase = _prior_rows(prior, "purchase_register")
        sales = _prior_rows(prior, "sales_register")
        bank = _prior_rows(prior, "bank_ledger")
        parsed = {
            "summary": (
                f"Master accounts workbook from {len(purchase)} purchase row(s), "
                f"{len(sales)} sales row(s), {len(bank)} bank row(s)."
            ),
            "artifacts": [
                {
                    "type": "master_accounts",
                    "title": "Master accounts (figures)",
                    "data": {
                        "purchase_rows": len(purchase),
                        "sales_rows": len(sales),
                        "bank_rows": len(bank),
                    },
                }
            ],
        }
        result_model = "parser:master_accounts"
    elif pack.feature_id == "tally-import-builder":
        parsed = {
            "summary": "Tally XML built from this client’s purchase register and bank ledger. Partner must approve before download.",
            "artifacts": [],
        }
        result_model = "parser:tally_xml"
    elif pack.feature_id == "gstr3b-review":
        books = _gstr3b_from_books(prior)
        if books:
            parsed = books
            result_model = "parser:gstr3b"
    elif pack.feature_id == "itc-reconcile":
        pr = _prior_rows(prior, "purchase_register")
        if pr:
            parsed = {
                "summary": f"ITC recon draft: {len(pr)} purchase row(s) marked PR-only until a GSTR-2B file is uploaded.",
                "artifacts": [
                    {
                        "type": "itc_recon",
                        "title": "ITC recon",
                        "data": {
                            "rows": [
                                {
                                    "vendor": r.get("vendor"),
                                    "invoice_no": r.get("invoice_no"),
                                    "total": r.get("total"),
                                    "code": "PR-only",
                                }
                                for r in pr
                            ]
                        },
                    },
                    {
                        "type": "exception_report",
                        "title": "Exceptions",
                        "data": {"items": ["Upload GSTR-2B Excel/JSON and run again to match 2B vs books."]},
                    },
                ],
            }
            result_model = "parser:itc"

    if parsed is None:
        try:
            result = complete(messages, effort=feature.get("effort") or "medium", feature_id=pack.feature_id)
        except Exception as exc:
            pack.status = "needs_review"
            pack.summary = f"Could not complete this job: {exc}"
            db.add(Message(workpack_id=pack.id, role="assistant", content=pack.summary))
            db.commit()
            db.refresh(pack)
            return pack
        parsed = result.parsed()
        if pack.feature_id == "bank-statement-processor":
            parsed = _ensure_bank_ledger(parsed, uploads)
        result_provider = result.provider
        result_model = result.model

    pack.model_used = f"{result_provider}:{result_model}"
    pack.summary = parsed.get("summary") or ""
    db.add(Message(workpack_id=pack.id, role="assistant", content=pack.summary))

    data_root = Path(settings.data_dir) / str(pack.firm_id) / str(pack.entity_id) / str(pack.id)
    data_root.mkdir(parents=True, exist_ok=True)

    for item in parsed.get("artifacts") or []:
        db.add(
            Artifact(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                entity_id=pack.entity_id,
                registration_id=pack.registration_id,
                period=pack.period,
                artifact_type=item.get("type") or "note",
                title=item.get("title") or item.get("type") or "Output",
                json_data=item.get("data"),
                is_input=False,
            )
        )

    if prior:
        db.add(
            Artifact(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                entity_id=pack.entity_id,
                registration_id=pack.registration_id,
                period=pack.period,
                artifact_type="reused_context",
                title="Reused from this client and period",
                json_data={
                    "types": [a.artifact_type for a in prior],
                    "titles": [a.title for a in prior],
                },
                is_input=False,
            )
        )

    if pack.feature_id == "tally-import-builder":
        rows = _prior_rows(prior, "purchase_register")
        xml = purchase_register_to_xml(rows, entity.tally_company or entity.name, pack.period)
        xml_path = data_root / "tally_import.xml"
        xml_path.write_text(xml, encoding="utf-8")
        db.add(
            Artifact(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                entity_id=pack.entity_id,
                registration_id=pack.registration_id,
                period=pack.period,
                artifact_type="tally_xml",
                title="Tally import XML",
                mime="application/xml",
                path=str(xml_path),
                is_input=False,
            )
        )

    if pack.feature_id == "master-accounts-sheet":
        xlsx_path = data_root / f"Master_Accounts_{pack.period or 'working'}.xlsx"
        meta = build_master_accounts(
            xlsx_path,
            company=entity.tally_company or entity.name,
            period=pack.period,
            purchase=_prior_rows(prior, "purchase_register"),
            sales=_prior_rows(prior, "sales_register"),
            bank=_prior_rows(prior, "bank_ledger"),
            opening=(_prior_data(prior, "bank_ledger") or {}).get("opening"),
            closing=(_prior_data(prior, "bank_ledger") or {}).get("closing"),
        )
        db.add(
            Artifact(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                entity_id=pack.entity_id,
                registration_id=pack.registration_id,
                period=pack.period,
                artifact_type="master_accounts_xlsx",
                title="Master Accounts workbook",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                path=str(xlsx_path),
                json_data=meta,
                is_input=False,
            )
        )

    _maybe_write_register_xlsx(db, pack, data_root, parsed)

    filing = feature.get("filing_class")
    if filing or (parsed.get("approval") or {}).get("kind"):
        kind = filing or parsed["approval"]["kind"]
        db.add(
            Approval(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                kind=kind,
                checklist=template_for(kind),
            )
        )
        pack.status = "pending_approval"
    else:
        pack.status = "needs_review"

    if pack.feature_id in ("notice-triage", "notice-analysis"):
        db.add(
            Notice(
                firm_id=pack.firm_id,
                entity_id=pack.entity_id,
                portal="gst" if registration and registration.kind == "gstin" else "income_tax",
                summary=pack.summary,
                status="in_progress",
            )
        )

    db.add(
        AuditEvent(
            firm_id=pack.firm_id,
            user_id=user.id,
            entity_id=pack.entity_id,
            workpack_id=pack.id,
            action="workpack.run",
            detail=pack.feature_id,
        )
    )
    db.commit()
    db.refresh(pack)
    return pack


def _reset_run_outputs(db: Session, pack: Workpack) -> None:
    db.query(Artifact).filter(Artifact.workpack_id == pack.id, Artifact.is_input.is_(False)).delete(
        synchronize_session=False
    )
    db.query(Message).filter(Message.workpack_id == pack.id, Message.role == "assistant").delete(
        synchronize_session=False
    )
    db.query(Approval).filter(Approval.workpack_id == pack.id, Approval.status == "pending").delete(
        synchronize_session=False
    )
    db.expire(pack, ["artifacts", "messages"])


def _ledger_has_rows(parsed: dict) -> bool:
    for item in parsed.get("artifacts") or []:
        if item.get("type") == "bank_ledger":
            data = item.get("data") or {}
            if data.get("rows"):
                return True
    return False


def _ensure_bank_ledger(parsed: dict, uploads: list[dict]) -> dict:
    if _ledger_has_rows(parsed):
        return parsed
    excerpt = "\n".join(u.get("text_excerpt") or "" for u in uploads)
    ledger = parse_bank_statement(excerpt)
    if not ledger.get("rows"):
        return parsed
    artifacts = list(parsed.get("artifacts") or [])
    artifacts.append({"type": "bank_ledger", "title": "Bank ledger", "data": ledger})
    parsed["artifacts"] = artifacts
    parsed["summary"] = (
        f"Extracted {len(ledger['rows'])} bank rows. "
        f"Opening {ledger.get('opening')}, closing {ledger.get('closing')}."
    )
    return parsed


def _prior_data(prior: list, typ: str) -> dict | None:
    for art in prior:
        if art.artifact_type == typ and isinstance(art.json_data, dict):
            return art.json_data
    return None


def _prior_rows(prior: list, typ: str) -> list:
    data = _prior_data(prior, typ) or {}
    return data.get("rows") or []


def _gstr3b_from_books(prior: list) -> dict | None:
    purchase = _prior_rows(prior, "purchase_register")
    sales = _prior_rows(prior, "sales_register")
    if not purchase and not sales:
        return None
    itc = 0.0
    for row in purchase:
        itc += float(row.get("cgst") or row.get("cgst_amount") or 0)
        itc += float(row.get("sgst") or row.get("sgst_amount") or 0)
        itc += float(row.get("igst") or row.get("igst_amount") or 0)
    outward = sum(float(row.get("taxable_value") or row.get("taxable") or 0) for row in sales)
    payable = max(outward * 0.18 - itc, 0)
    return {
        "summary": "GSTR-3B working from books on this client and period. Partner must approve. Nothing is filed.",
        "artifacts": [
            {
                "type": "gstr3b_working",
                "title": "GSTR-3B working (from books)",
                "data": {
                    "outward_taxable": outward,
                    "itc_available": itc,
                    "tax_payable": payable,
                    "notes": [
                        "Draft only — not filed.",
                        "Outward tax uses 18% on sales-register taxable value when rates are not line-wise.",
                    ],
                },
            }
        ],
        "approval": {"kind": "gst_filing"},
    }


def _maybe_write_register_xlsx(db: Session, pack: Workpack, data_root: Path, parsed: dict) -> None:
    for item in parsed.get("artifacts") or []:
        rows = (item.get("data") or {}).get("rows") if isinstance(item.get("data"), dict) else None
        if not rows:
            continue
        if item.get("type") == "purchase_register":
            headers, table = purchase_rows_table(rows)
            path = data_root / "purchase_register.xlsx"
            write_rows_xlsx(path, "PURCHASE", headers, table)
            title = "Purchase register.xlsx"
        elif item.get("type") == "bank_ledger":
            headers, table = bank_rows_table(rows)
            path = data_root / "bank_ledger.xlsx"
            write_rows_xlsx(path, "BANK", headers, table)
            title = "Bank ledger.xlsx"
        else:
            continue
        db.add(
            Artifact(
                firm_id=pack.firm_id,
                workpack_id=pack.id,
                entity_id=pack.entity_id,
                registration_id=pack.registration_id,
                period=pack.period,
                artifact_type="workbook",
                title=title,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                path=str(path),
                is_input=False,
            )
        )

