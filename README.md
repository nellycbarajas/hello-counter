# hello-counter

Minimal counter service. End-to-end validation harness for esencIA.

## What it is

A single counter persisted in SQLite, with three HTTP endpoints and a
one-button UI. Built to exercise every phase of esencIA (definition,
architecture, devops, governance, release) on a project small enough to
be broken on purpose.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/count` | Returns current counter value as `{ "value": <int> }` |
| POST | `/increment` | Increments the counter; returns `{ "value", "updated_at" }` |
| GET | `/health` | Returns `{"status":"ok"}` (200) or `{"status":"degraded"}` (500) |
| GET | `/` | Static single-page UI |

## Local development

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# browse http://127.0.0.1:8000/
```

## Tests

```bash
pytest --cov=app
```

Coverage floor is 80% (enforced by CI via `pyproject.toml`).

## Docker

```bash
docker compose up -d --build
curl -fsS http://127.0.0.1:8000/health
```

## Governance artifacts

| File | Governs |
|------|---------|
| `memory/project_brief.md` | MVP scope, discovery, UX, data model (sealed) |
| `memory/project_tech_profile.md` | Stack (`TECHNOLOGY_POLICY.md`) |
| `memory/project_architecture_profile.md` | Axes A/B/C (`ARCHITECTURE_POLICY.md`) |
| `memory/project_devops_profile.md` | Pipeline + gates (`DEVOPS_POLICY.md`) |
| `memory/ui_ux_definition.md` | Visual direction (`UX_UI_POLICY.md`) |
| `memory/decision_log.md` | ADRs (append-only) |
| `memory/release_state.json` | Release number, stories, status |
| `memory/risk_register.json` | Open risks |
| `memory/metrics.json` | Planned vs actual |
| `memory/global_rules.md` | Snapshot of core rules at bootstrap |

## Architecture at a glance

- **System style:** `modular_monolith` (default per `ARCHITECTURE_POLICY.md`).
- **Internal structure:** `layered` — presentation (`app/main.py`) → domain (`app/domain/`) → infrastructure (`app/infrastructure/`). Justified by ADR-002.
- **Supporting patterns:** none.

## Next steps (operator)

Run `docs/DEVOPS_VALIDATION_CHECKLIST.md` against this repo end-to-end
to exercise all six failure-injection tests plus rollback.
