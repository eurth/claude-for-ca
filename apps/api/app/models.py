import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def uuid_pk():
    return mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)


JSONType = JSON().with_variant(JSONB, "postgresql")


class Firm(Base):
    __tablename__ = "firms"

    id = uuid_pk()
    name: Mapped[str] = mapped_column(String(255))
    ca_name: Mapped[str] = mapped_column(String(255))
    gstin: Mapped[str | None] = mapped_column(String(15), nullable=True)
    membership_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    firm_reg_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    jurisdiction: Mapped[str | None] = mapped_column(String(128), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    hitl_threshold: Mapped[int] = mapped_column(Integer, default=100000)
    default_llm_provider: Mapped[str] = mapped_column(String(32), default="mock")
    letterhead: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    users = relationship("User", back_populates="firm")


class User(Base):
    __tablename__ = "users"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32))  # partner | manager | intern
    password_hash: Mapped[str] = mapped_column(String(255))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    firm = relationship("Firm", back_populates="users")
    __table_args__ = (UniqueConstraint("firm_id", "email"),)


class ClientGroup(Base):
    __tablename__ = "client_groups"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    name: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class LegalEntity(Base):
    __tablename__ = "legal_entities"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    group_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("client_groups.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    pan: Mapped[str | None] = mapped_column(String(10), nullable=True)
    cin: Mapped[str | None] = mapped_column(String(21), nullable=True)
    entity_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    jurisdiction: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tally_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    registrations = relationship("Registration", back_populates="entity")
    __table_args__ = (
        UniqueConstraint("firm_id", "pan"),
        Index("ix_entities_firm", "firm_id"),
    )


class Registration(Base):
    __tablename__ = "registrations"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("legal_entities.id"))
    kind: Mapped[str] = mapped_column(String(16))  # gstin | tan | pf | esic
    value: Mapped[str] = mapped_column(String(32))
    state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    filing_cadence: Mapped[str | None] = mapped_column(String(32), nullable=True)
    label: Mapped[str | None] = mapped_column(String(128), nullable=True)

    entity = relationship("LegalEntity", back_populates="registrations")
    __table_args__ = (
        UniqueConstraint("firm_id", "kind", "value"),
        Index("ix_registrations_entity", "entity_id"),
    )


class Workpack(Base):
    __tablename__ = "workpacks"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("legal_entities.id"))
    registration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("registrations.id"), nullable=True)
    feature_id: Mapped[str] = mapped_column(String(64))
    period: Mapped[str | None] = mapped_column(String(32), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="draft")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    artifacts = relationship("Artifact", back_populates="workpack")
    messages = relationship("Message", back_populates="workpack")
    __table_args__ = (Index("ix_workpacks_firm_entity", "firm_id", "entity_id"),)


class Artifact(Base):
    __tablename__ = "artifacts"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    workpack_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workpacks.id"))
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("legal_entities.id"))
    registration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("registrations.id"), nullable=True)
    period: Mapped[str | None] = mapped_column(String(32), nullable=True)
    artifact_type: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    mime: Mapped[str | None] = mapped_column(String(128), nullable=True)
    path: Mapped[str | None] = mapped_column(Text, nullable=True)
    json_data: Mapped[dict | None] = mapped_column(JSONType, nullable=True)
    is_input: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    workpack = relationship("Workpack", back_populates="artifacts")
    __table_args__ = (
        Index("ix_artifacts_reuse", "firm_id", "entity_id", "artifact_type", "period"),
        Index("ix_artifacts_workpack", "workpack_id"),
    )


class Message(Base):
    __tablename__ = "messages"

    id = uuid_pk()
    workpack_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workpacks.id"))
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    workpack = relationship("Workpack", back_populates="messages")


class Approval(Base):
    __tablename__ = "approvals"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    workpack_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workpacks.id"))
    kind: Mapped[str] = mapped_column(String(32))
    checklist: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    decided_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    __table_args__ = (Index("ix_approvals_firm_status", "firm_id", "status"),)


class Notice(Base):
    __tablename__ = "notices"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    entity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("legal_entities.id"))
    portal: Mapped[str] = mapped_column(String(32))
    section: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notice_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    demand_amount: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    due_date: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="received")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class CalendarTask(Base):
    __tablename__ = "calendar_tasks"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    entity_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("legal_entities.id"), nullable=True)
    registration_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("registrations.id"), nullable=True)
    form_type: Mapped[str] = mapped_column(String(64))
    period: Mapped[str | None] = mapped_column(String(32), nullable=True)
    due_date: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = uuid_pk()
    firm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("firms.id"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("legal_entities.id"), nullable=True)
    workpack_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("workpacks.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(64))
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
