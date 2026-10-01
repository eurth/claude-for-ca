from fastapi import APIRouter, Depends

from app.deps import current_user
from app.models import User
from app.runtime.catalog import CATALOG

router = APIRouter(prefix="/api/features", tags=["features"])


@router.get("")
def list_features(user: User = Depends(current_user)):
    return {"features": CATALOG}
