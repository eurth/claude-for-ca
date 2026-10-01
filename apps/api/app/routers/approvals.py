from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_roles
from app.models import Approval, AuditEvent, User, Workpack

router = APIRouter(prefix="/api/approvals", tags=["approvals"])


@router.get("")
def list_approvals(user: User = Depends(require_roles("partner", "manager")), db: Session = Depends(get_db)):
    rows = (
        db.query(Approval)
        .filter(Approval.firm_id == user.firm_id, Approval.status == "pending")
        .order_by(Approval.created_at.desc())
        .all()
    )
    out = []
    for a in rows:
        p = db.get(Workpack, a.workpack_id)
        out.append(
            {
                "id": str(a.id),
                "kind": a.kind,
                "checklist": a.checklist,
                "workpack_id": str(a.workpack_id),
                "title": p.title if p else "",
                "status": a.status,
            }
        )
    return {"approvals": out}


class DecisionIn(BaseModel):
    decision: str
    note: str | None = None


@router.post("/{approval_id}")
def decide(
    approval_id: UUID,
    body: DecisionIn,
    user: User = Depends(require_roles("partner")),
    db: Session = Depends(get_db),
):
    a = db.get(Approval, approval_id)
    if not a or a.firm_id != user.firm_id:
        raise HTTPException(404, "Approval not found")
    if body.decision not in ("approve", "deny"):
        raise HTTPException(400, "Decision must be approve or deny")
    a.status = "approved" if body.decision == "approve" else "denied"
    a.decided_by = user.id
    a.decided_at = datetime.now(timezone.utc)
    a.note = body.note
    pack = db.get(Workpack, a.workpack_id)
    if pack:
        pack.status = "approved" if a.status == "approved" else "denied"
    db.add(
        AuditEvent(
            firm_id=user.firm_id,
            user_id=user.id,
            workpack_id=a.workpack_id,
            action=f"approval.{a.status}",
            detail=a.kind,
        )
    )
    db.commit()
    return {"status": a.status}
