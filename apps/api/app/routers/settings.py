from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings as env
from app.db import get_db
from app.deps import current_user, require_roles
from app.models import Firm, User

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_settings(user: User = Depends(current_user), db: Session = Depends(get_db)):
    firm = db.get(Firm, user.firm_id)
    out = {
        "firm_name": firm.name if firm else "",
        "ca_name": firm.ca_name if firm else "",
        "hitl_threshold": firm.hitl_threshold if firm else 100000,
        "letterhead": firm.letterhead if firm else None,
        "jurisdiction": firm.jurisdiction if firm else None,
    }
    if user.role == "partner":
        out["llm_provider"] = env.llm_provider
        out["providers_configured"] = {
            "openrouter": bool(env.openrouter_api_key),
            "anthropic": bool(env.anthropic_api_key),
            "openai": bool(env.openai_api_key),
            "gemini": bool(env.gemini_api_key),
        }
    return out


class SettingsIn(BaseModel):
    hitl_threshold: int | None = None
    letterhead: str | None = None
    default_llm_provider: str | None = None


@router.patch("")
def patch_settings(
    body: SettingsIn,
    user: User = Depends(require_roles("partner")),
    db: Session = Depends(get_db),
):
    firm = db.get(Firm, user.firm_id)
    if body.hitl_threshold is not None:
        firm.hitl_threshold = body.hitl_threshold
    if body.letterhead is not None:
        firm.letterhead = body.letterhead
    if body.default_llm_provider in ("mock", "anthropic", "openai", "gemini", "openrouter"):
        firm.default_llm_provider = body.default_llm_provider
    db.commit()
    return {"ok": True}
