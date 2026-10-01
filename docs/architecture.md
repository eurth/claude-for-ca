# Architecture — for-ca

Eurth-hosted web app: staff UI + FastAPI runtime + Postgres + file volume + pluggable LLM gateway. Skill markdown stays the CA brain.

## System

```
Staff browser
    → Next.js (apps/web)     firm chrome, roles, workpacks
    → FastAPI (apps/api)     auth, entities, files, skill run, HITL
         ├─ SkillRuntime     loads packs/*.md, injects context
         ├─ LLMGateway       Anthropic | OpenAI | Gemini | mock
         ├─ Postgres         tenants, entities, workpacks, artifacts
         └─ Volume           /app/data  ←  /data/ca-practice-data
```

Claude Code plugins, hooks, and Desktop Projects are **not** on the request path.

## Repository layout

```
apps/api/          FastAPI, SQLAlchemy, runtime, HITL
apps/web/          Next.js App Router
packs/             Canonical SKILL.md for the six pilots (Claude interpolators stripped)
docs/              Product + inventory + this file
docs/infra/        Coolify deployment guide
Dockerfile         API image (uvicorn)
docker-compose.yml db + api + web
coolify.env.example
```

Existing plugin folders (`gst-compliance/`, etc.) remain the long-term procedure source. Phase 2 pilots are copied into `packs/` so the API does not depend on `${CLAUDE_PLUGIN_ROOT}`.

## Data (Postgres)

Mapped from the SQLite memory bank, with hierarchy added:

- `firms` — tenant
- `users` — email, role (`partner` | `manager` | `intern`), hashed password
- `client_groups`
- `legal_entities` — PAN unique per firm
- `registrations` — kind `gstin` | `tan` | `pf` | `esic`
- `periods` — optional cache; periods may also be strings on workpacks
- `workpacks` — feature_id, entity, registration, period, status, model used
- `artifacts` — type, json/path, workpack_id, entity/registration/period keys
- `messages` — workpack thread
- `approvals` — HITL checklist, decision
- `notices`, `calendar_tasks`, `audit_events`
- `firm_settings` — HITL threshold, default provider (API keys live in env, not DB)

## Skill run

1. Client POSTs `/api/workpacks/{id}/run` with optional extra files.
2. Runtime loads `packs/<feature>/SKILL.md`.
3. Bundles firm + entity + registration + period + reusable artifacts.
4. Calls `LLMGateway.complete(messages, tools)`.
5. Tools allowed in v1: `save_artifact`, `create_approval`, `log_audit`, `log_notice` — **no** portal submit, **no** Tally post.
6. Filing-class features always `create_approval` with the matching HITL template.
7. Status → `needs_review` or `pending_approval`.

## LLM gateway

| Provider | Env | When used |
|----------|-----|-----------|
| `anthropic` | `ANTHROPIC_API_KEY` | Default if set |
| `openai` | `OPENAI_API_KEY` | Alternate |
| `gemini` | `GEMINI_API_KEY` | Alternate |
| `mock` | none | Local/dev; returns structured draft JSON so the UI works without keys |

Routing: feature catalog `effort` (`low` → cheap model, `high` → strong). Partner settings pick provider. Interns never see this.

## HITL

Replace `hooks.json` with table `approvals`:

- `gst_filing`, `tds_filing`, `itr_filing`, `mca_filing`, `tally_write`, `notice_send`
- Checklist text ported from `shared/bin/hitl-*.sh`
- Partner `approve` | `deny`; intern cannot

v1 approve means “ready to download / ready to send outside the app”, not “submit to portal”.

## Auth

JWT after email/password. Seed Partner for Gorantla on first boot (`seed_cloud.py` pattern from the Coolify guide). All routes scoped by `firm_id`.

## Files

Uploads stored under `/app/data/firms/{firm_id}/entities/{entity_id}/...` on the Docker volume. Original PDFs hashed; artifacts may be JSON in Postgres when small, files when xlsx/xml.

## Deploy (Coolify)

Follow [docs/infra/EURTHTECH_DEPLOYMENT_GUIDE.md](infra/EURTHTECH_DEPLOYMENT_GUIDE.md).

| Item | Value |
|------|--------|
| Subdomain | `https://ca.eurthtech.com` |
| Build | Docker Compose (web + api) or API image + static web |
| Internal ports | API `8510`, web `8511` (8503–8504 taken) |
| Volume | `/data/ca-practice-data` → `/app/data` |
| Database | Coolify Postgres resource → `DATABASE_URL` |
| Secrets | `JWT_SECRET`, LLM keys — Coolify vault, never git |
| DNS | Wix A record `ca` → `172.236.176.222` |
| Auto-deploy | push `main` |

Do not use DuckDB/SQLite for production: concurrent staff writes. Postgres is required.

## Security

- PAN/Aadhaar not written to `audit_events.input_summary` in full (mask).
- Passwords hashed (bcrypt).
- Filing tools absent from the v1 tool list even if a skill markdown mentions submit.
- CORS limited to the web origin.
