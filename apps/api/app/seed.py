from sqlalchemy.orm import Session

from app.auth import hash_password
from app.config import settings
from app.models import (
    CalendarTask,
    ClientGroup,
    Firm,
    LegalEntity,
    Registration,
    User,
)


def seed_if_empty(db: Session) -> None:
    if db.query(Firm).first():
        return

    firm = Firm(
        name=settings.seed_firm_name,
        ca_name=settings.seed_ca_name,
        jurisdiction="Andhra Pradesh",
        hitl_threshold=settings.seed_hitl_threshold,
        default_llm_provider=settings.llm_provider,
    )
    db.add(firm)
    db.flush()

    db.add(
        User(
            firm_id=firm.id,
            email=settings.seed_partner_email.lower(),
            name=settings.seed_ca_name,
            role="partner",
            password_hash=hash_password(settings.seed_partner_password),
        )
    )
    db.add(
        User(
            firm_id=firm.id,
            email="intern@gorantla.local",
            name="Articleship intern",
            role="intern",
            password_hash=hash_password(settings.seed_partner_password),
        )
    )
    db.add(
        User(
            firm_id=firm.id,
            email="manager@gorantla.local",
            name="Practice manager",
            role="manager",
            password_hash=hash_password(settings.seed_partner_password),
        )
    )

    group = ClientGroup(firm_id=firm.id, name="Sample manufacturing group")
    db.add(group)
    db.flush()

    entity = LegalEntity(
        firm_id=firm.id,
        group_id=group.id,
        name="Example Traders Pvt Ltd",
        pan="AACTE1234F",
        cin="U21000AP2018PTC000001",
        entity_type="Private Ltd",
        industry="Trading",
        jurisdiction="Andhra Pradesh",
        tally_company="Example Traders Pvt Ltd",
        contact_name="Accounts in-charge",
    )
    db.add(entity)
    db.flush()

    gstin = Registration(
        firm_id=firm.id,
        entity_id=entity.id,
        kind="gstin",
        value="37AACTE1234F1Z5",
        state="Andhra Pradesh",
        filing_cadence="monthly",
        label="Head office",
    )
    db.add(gstin)
    db.add(
        Registration(
            firm_id=firm.id,
            entity_id=entity.id,
            kind="gstin",
            value="29AACTE1234F1Z4",
            state="Karnataka",
            filing_cadence="monthly",
            label="Bengaluru branch",
        )
    )
    db.add(
        Registration(
            firm_id=firm.id,
            entity_id=entity.id,
            kind="tan",
            value="HYDE12345F",
            label="TAN",
        )
    )
    db.flush()

    db.add(
        CalendarTask(
            firm_id=firm.id,
            entity_id=entity.id,
            registration_id=gstin.id,
            form_type="GSTR-3B",
            period="2026-04",
            due_date="2026-05-20",
            description="Monthly GSTR-3B",
        )
    )
    db.commit()
