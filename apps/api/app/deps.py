from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth import decode_token
from app.db import get_db
from app.models import User

bearer = HTTPBearer(auto_error=False)


def current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if creds is None:
        raise HTTPException(401, "Sign in required")
    try:
        payload = decode_token(creds.credentials)
    except ValueError:
        raise HTTPException(401, "Session expired — please sign in again")
    user = db.get(User, UUID(payload["sub"]))
    if not user or not user.active:
        raise HTTPException(401, "Account not found")
    return user


def require_roles(*roles: str):
    def checker(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "This action is for a Partner or Manager")
        return user

    return checker
