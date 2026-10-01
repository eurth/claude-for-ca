from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.routers import approvals, audit, auth, clients, features, home, workpacks
from app.routers import settings as settings_router
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="for-ca", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_origin, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(clients.router)
app.include_router(features.router)
app.include_router(workpacks.router)
app.include_router(approvals.router)
app.include_router(audit.router)
app.include_router(settings_router.router)


@app.get("/health")
def health():
    provider = (settings.llm_provider or "mock").lower()
    configured = bool(
        (provider == "openrouter" and settings.openrouter_api_key)
        or (provider == "anthropic" and settings.anthropic_api_key)
        or (provider == "openai" and settings.openai_api_key)
        or (provider == "gemini" and settings.gemini_api_key)
    )
    return {
        "ok": True,
        "name": "for-ca",
        "llm_provider": provider if configured else "mock",
    }


@app.get("/api/gateway")
def gateway_status():
    return {
        "provider": settings.llm_provider,
        "openrouter": bool(settings.openrouter_api_key),
    }
