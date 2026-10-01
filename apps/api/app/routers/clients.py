from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import current_user, require_roles
from app.models import CalendarTask, ClientGroup, LegalEntity, Notice, Registration, User

router = APIRouter(prefix="/api/clients", tags=["clients"])


def _entity_out(e: LegalEntity, regs: list[Registration]) -> dict:
    return {
        "id": str(e.id),
        "group_id": str(e.group_id) if e.group_id else None,
        "name": e.name,
        "pan": e.pan,
        "cin": e.cin,
        "entity_type": e.entity_type,
        "industry": e.industry,
        "tally_company": e.tally_company,
        "active": e.active,
        "registrations": [
            {
                "id": str(r.id),
                "kind": r.kind,
                "value": r.value,
                "state": r.state,
                "filing_cadence": r.filing_cadence,
                "label": r.label,
            }
            for r in regs
            if r.entity_id == e.id
        ],
    }


@router.get("")
def list_clients(user: User = Depends(current_user), db: Session = Depends(get_db)):
    groups = db.query(ClientGroup).filter(ClientGroup.firm_id == user.firm_id).all()
    entities = db.query(LegalEntity).filter(LegalEntity.firm_id == user.firm_id).all()
    regs = db.query(Registration).filter(Registration.firm_id == user.firm_id).all()
    return {
        "groups": [{"id": str(g.id), "name": g.name} for g in groups],
        "entities": [_entity_out(e, regs) for e in entities],
    }


@router.get("/{entity_id}")
def get_entity(entity_id: UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    e = db.get(LegalEntity, entity_id)
    if not e or e.firm_id != user.firm_id:
        raise HTTPException(404, "Client not found")
    regs = db.query(Registration).filter(Registration.entity_id == e.id).all()
    tasks = (
        db.query(CalendarTask)
        .filter(
            CalendarTask.entity_id == e.id,
            CalendarTask.firm_id == user.firm_id,
            CalendarTask.status == "pending",
        )
        .all()
    )
    out = _entity_out(e, regs)
    out["dues"] = [
        {"form_type": t.form_type, "period": t.period, "due_date": t.due_date, "description": t.description}
        for t in tasks
    ]
    notices = (
        db.query(Notice)
        .filter(Notice.entity_id == e.id, Notice.firm_id == user.firm_id)
        .order_by(Notice.created_at.desc())
        .limit(20)
        .all()
    )
    out["notices"] = [
        {
            "id": str(n.id),
            "portal": n.portal,
            "summary": n.summary,
            "status": n.status,
            "due_date": n.due_date,
        }
        for n in notices
    ]
    return out


class EntityIn(BaseModel):
    name: str
    pan: str | None = None
    cin: str | None = None
    entity_type: str | None = None
    industry: str | None = None
    group_name: str | None = None
    gstin: str | None = None
    gstin_state: str | None = None
    gst_cadence: str | None = "monthly"
    tan: str | None = None
    tally_company: str | None = None


@router.post("")
def create_entity(
    body: EntityIn,
    user: User = Depends(require_roles("partner", "manager")),
    db: Session = Depends(get_db),
):
    group_id = None
    if body.group_name:
        g = (
            db.query(ClientGroup)
            .filter(ClientGroup.firm_id == user.firm_id, ClientGroup.name == body.group_name)
            .first()
        )
        if not g:
            g = ClientGroup(firm_id=user.firm_id, name=body.group_name)
            db.add(g)
            db.flush()
        group_id = g.id
    e = LegalEntity(
        firm_id=user.firm_id,
        group_id=group_id,
        name=body.name,
        pan=(body.pan or "").upper() or None,
        cin=body.cin,
        entity_type=body.entity_type,
        industry=body.industry,
        tally_company=body.tally_company or body.name,
    )
    db.add(e)
    db.flush()
    if body.gstin:
        db.add(
            Registration(
                firm_id=user.firm_id,
                entity_id=e.id,
                kind="gstin",
                value=body.gstin.upper(),
                state=body.gstin_state,
                filing_cadence=body.gst_cadence,
                label="GSTIN",
            )
        )
    if body.tan:
        db.add(
            Registration(
                firm_id=user.firm_id,
                entity_id=e.id,
                kind="tan",
                value=body.tan.upper(),
                label="TAN",
            )
        )
    db.commit()
    return {"id": str(e.id)}


class RegistrationIn(BaseModel):
    kind: str = "gstin"
    value: str
    state: str | None = None
    filing_cadence: str | None = "monthly"
    label: str | None = None


@router.post("/{entity_id}/registrations")
def add_registration(
    entity_id: UUID,
    body: RegistrationIn,
    user: User = Depends(require_roles("partner", "manager")),
    db: Session = Depends(get_db),
):
    e = db.get(LegalEntity, entity_id)
    if not e or e.firm_id != user.firm_id:
        raise HTTPException(404, "Client not found")
    if body.kind not in ("gstin", "tan", "pf", "esic"):
        raise HTTPException(400, "Registration kind must be gstin, tan, pf or esic")
    db.add(
        Registration(
            firm_id=user.firm_id,
            entity_id=e.id,
            kind=body.kind,
            value=body.value.upper(),
            state=body.state,
            filing_cadence=body.filing_cadence,
            label=body.label or body.kind.upper(),
        )
    )
    db.commit()
    return {"ok": True}
