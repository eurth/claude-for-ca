from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import current_user
from app.models import Approval, CalendarTask, LegalEntity, User, Workpack

router = APIRouter(prefix="/api/home", tags=["home"])


@router.get("")
def home(user: User = Depends(current_user), db: Session = Depends(get_db)):
    dues = (
        db.query(CalendarTask)
        .filter(CalendarTask.firm_id == user.firm_id, CalendarTask.status == "pending")
        .limit(20)
        .all()
    )
    packs = (
        db.query(Workpack)
        .filter(Workpack.firm_id == user.firm_id)
        .order_by(Workpack.created_at.desc())
        .limit(10)
        .all()
    )
    pending = (
        db.query(Approval)
        .filter(Approval.firm_id == user.firm_id, Approval.status == "pending")
        .count()
    )
    entities = {str(e.id): e.name for e in db.query(LegalEntity).filter(LegalEntity.firm_id == user.firm_id)}
    return {
        "pending_approvals": pending,
        "dues": [
            {
                "form_type": t.form_type,
                "period": t.period,
                "due_date": t.due_date,
                "entity": entities.get(str(t.entity_id), ""),
            }
            for t in dues
        ],
        "recent": [
            {
                "id": str(p.id),
                "title": p.title,
                "status": p.status,
                "entity": entities.get(str(p.entity_id), ""),
            }
            for p in packs
        ],
    }
