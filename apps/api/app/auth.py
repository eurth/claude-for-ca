import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings


def hash_password(plain: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, 120_000)
    return base64.b64encode(salt + dk).decode("ascii")


def verify_password(plain: str, hashed: str) -> bool:
    raw = base64.b64decode(hashed.encode("ascii"))
    salt, dk = raw[:16], raw[16:]
    check = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(dk, check)


def create_token(user_id: str, firm_id: str, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_hours)
    return jwt.encode(
        {"sub": user_id, "firm": firm_id, "role": role, "exp": exp},
        settings.jwt_secret,
        algorithm="HS256",
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError as exc:
        raise ValueError("Invalid session") from exc
