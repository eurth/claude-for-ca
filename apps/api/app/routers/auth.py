from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import create_token, verify_password
from app.db import get_db
from app.deps import current_user
from app.models import Firm, User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == body.email.lower())
        .first()
    )
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Email or password is incorrect")
    firm = db.get(Firm, user.firm_id)
    token = create_token(str(user.id), str(user.firm_id), user.role)
    return {
        "token": token,
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "firm_name": firm.name if firm else "",
            "firm_id": str(user.firm_id),
        },
    }


@router.get("/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)):
    firm = db.get(Firm, user.firm_id)
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "firm_name": firm.name if firm else "",
        "firm_id": str(user.firm_id),
        "hitl_threshold": firm.hitl_threshold if firm else 100000,
        "llm_provider": firm.default_llm_provider if firm else "mock",
    }
