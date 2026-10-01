from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import current_user
from app.models import AuditEvent, User

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("")
def list_audit(user: User = Depends(current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(AuditEvent)
        .filter(AuditEvent.firm_id == user.firm_id)
        .order_by(AuditEvent.created_at.desc())
        .limit(100)
        .all()
    )
    return {
        "events": [
            {
                "id": str(e.id),
                "action": e.action,
                "detail": e.detail if user.role == "partner" else (e.detail or "").split(" via ")[0],
                "at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in rows
        ]
    }
