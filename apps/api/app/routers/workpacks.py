from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.deps import current_user
from app.models import Approval, Artifact, LegalEntity, Message, User, Workpack
from app.runtime.catalog import get_feature
from app.runtime.runner import run_workpack

router = APIRouter(prefix="/api/workpacks", tags=["workpacks"])


def _pack_out(db: Session, p: Workpack) -> dict:
    arts = db.query(Artifact).filter(Artifact.workpack_id == p.id).all()
    msgs = db.query(Message).filter(Message.workpack_id == p.id).order_by(Message.created_at).all()
    return {
        "id": str(p.id),
        "feature_id": p.feature_id,
        "title": p.title,
        "status": p.status,
        "period": p.period,
        "summary": p.summary,
        "entity_id": str(p.entity_id),
        "registration_id": str(p.registration_id) if p.registration_id else None,
        "artifacts": [
            {
                "id": str(a.id),
                "type": a.artifact_type,
                "title": a.title,
                "is_input": a.is_input,
                "has_file": bool(a.path),
                "json": a.json_data,
            }
            for a in arts
        ],
        "messages": [{"role": m.role, "content": m.content} for m in msgs],
        "approvals": [
            {
                "id": str(a.id),
                "kind": a.kind,
                "status": a.status,
                "checklist": a.checklist,
            }
            for a in db.query(Approval).filter(Approval.workpack_id == p.id).all()
        ],
    }


class PackIn(BaseModel):
    feature_id: str
    entity_id: UUID
    registration_id: UUID | None = None
    period: str | None = None
    note: str | None = None

    @field_validator("registration_id", "note", "period", mode="before")
    @classmethod
    def blank_to_none(cls, v):
        if v == "":
            return None
        return v


@router.get("")
def list_packs(entity_id: UUID | None = None, user: User = Depends(current_user), db: Session = Depends(get_db)):
    q = db.query(Workpack).filter(Workpack.firm_id == user.firm_id)
    if entity_id:
        q = q.filter(Workpack.entity_id == entity_id)
    rows = q.order_by(Workpack.created_at.desc()).limit(50).all()
    return {
        "workpacks": [
            {
                "id": str(p.id),
                "title": p.title,
                "feature_id": p.feature_id,
                "status": p.status,
                "period": p.period,
                "entity_id": str(p.entity_id),
            }
            for p in rows
        ]
    }


@router.post("")
def create_pack(body: PackIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    try:
        feature = get_feature(body.feature_id)
    except KeyError:
        raise HTTPException(400, "Unknown feature")
    entity = db.get(LegalEntity, body.entity_id)
    if not entity or entity.firm_id != user.firm_id:
        raise HTTPException(404, "Client not found")
    if feature["scope"] == "gstin" and not body.registration_id:
        raise HTTPException(400, "Select a GSTIN for this job")
    title = f"{feature['name']}" + (f" — {body.period}" if body.period else "")
    pack = Workpack(
        firm_id=user.firm_id,
        entity_id=entity.id,
        registration_id=body.registration_id,
        feature_id=body.feature_id,
        period=body.period,
        title=title,
        created_by=user.id,
    )
    db.add(pack)
    db.flush()
    if body.note:
        db.add(Message(workpack_id=pack.id, role="user", content=body.note))
    db.commit()
    return {"id": str(pack.id)}


@router.get("/{pack_id}")
def get_pack(pack_id: UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    pack = db.get(Workpack, pack_id)
    if not pack or pack.firm_id != user.firm_id:
        raise HTTPException(404, "Workpack not found")
    out = _pack_out(db, pack)
    if user.role == "partner":
        out["model_used"] = pack.model_used
    return out


@router.post("/{pack_id}/files")
async def upload_file(
    pack_id: UUID,
    upload: UploadFile = File(...),
    artifact_type: str = Form("upload"),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    pack = db.get(Workpack, pack_id)
    if not pack or pack.firm_id != user.firm_id:
        raise HTTPException(404, "Workpack not found")
    dest_dir = settings.data_dir / str(pack.firm_id) / str(pack.entity_id) / str(pack.id) / "in"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (upload.filename or "upload.bin")
    dest.write_bytes(await upload.read())
    db.add(
        Artifact(
            firm_id=pack.firm_id,
            workpack_id=pack.id,
            entity_id=pack.entity_id,
            registration_id=pack.registration_id,
            period=pack.period,
            artifact_type=artifact_type,
            title=upload.filename or "upload",
            mime=upload.content_type,
            path=str(dest),
            is_input=True,
        )
    )
    db.commit()
    return {"ok": True}


@router.post("/{pack_id}/run")
def run_pack(pack_id: UUID, user: User = Depends(current_user), db: Session = Depends(get_db)):
    pack = db.get(Workpack, pack_id)
    if not pack or pack.firm_id != user.firm_id:
        raise HTTPException(404, "Workpack not found")
    pack = run_workpack(db, pack, user)
    return _pack_out(db, pack)


@router.get("/{pack_id}/files/{artifact_id}")
def download_artifact(
    pack_id: UUID,
    artifact_id: UUID,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    from fastapi.responses import FileResponse

    pack = db.get(Workpack, pack_id)
    art = db.get(Artifact, artifact_id)
    if not pack or not art or pack.firm_id != user.firm_id or art.workpack_id != pack.id:
        raise HTTPException(404, "File not found")
    if not art.path:
        raise HTTPException(404, "No file on this output")
    if art.artifact_type == "tally_xml" and pack.status != "approved":
        raise HTTPException(403, "Partner must approve this file before download")
    return FileResponse(art.path, filename=art.title.replace(" ", "_") + (".xml" if art.artifact_type == "tally_xml" else ""))
