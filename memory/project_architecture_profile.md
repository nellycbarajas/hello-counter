# Architecture Profile — hello-counter

> Aligned with `/esencIA/core/ARCHITECTURE_POLICY.md`. Filled during Phase 3.

## 1. Project Identification

| Field | Value |
|-------|-------|
| Project name | hello-counter |
| Slug | hello-counter |
| Owner (human — accountable) | platform |
| Architecture lead (human — responsible) | platform |
| Created | 2026-04-22 |
| Profile version | `1.0` |
| Last updated | 2026-04-22 |

## 2. Architecture Shape (the three axes)

Per `ARCHITECTURE_POLICY.md §2`.

### Axis A — System architecture style

- [x] `modular_monolith` _(default)_
- [ ] `service_oriented_application`
- [ ] `microservices`
- [ ] `event_driven`
- [ ] `serverless_oriented`

**Triggered by rule(s):** none — default applies.

### Axis B — Internal application structure

- [x] `layered`
- [ ] `hexagonal`
- [ ] `clean_architecture`

**Triggered by rule(s):** B.1 — MVP under 6 weeks, team ≤ 2 engineers.

### Axis C — Supporting patterns

- [ ] `backend_for_frontend`
- [ ] `workflow_centric`
- [ ] `ai_augmented`

No supporting patterns adopted.

## 3. Deviations from defaults

| Axis | Default | Chosen | ADR | Justification |
|---|---|---|---|---|
| B | `hexagonal` (preferred for business apps) | `layered` | ADR-002 | Rule B.1 fires — MVP ≤ 6 weeks, team of 1 engineer. One adapter (SQLite). The isolation cost of hexagonal is not justified. |

## 4. Boundaries and modules (Axis A detail)

Single deployable unit (FastAPI container). Internal modules:

| Module | Responsibility | Public contract |
|---|---|---|
| `app/main.py` | FastAPI app + static file serving + route wiring | HTTP routes |
| `app/domain/counter.py` | Pure counter value logic (increment, validate) | Python functions, no framework imports |
| `app/infrastructure/repository.py` | SQLite persistence | `CounterRepository` class |
| `app/config.py` | Env-based configuration loader | `Settings` dataclass |

## 5. Internal structure detail (Axis B detail)

### 5.1 Dependency direction

`layered`: `presentation (main.py) → application (implicit in routes) → domain (counter.py) → infrastructure (repository.py)`.

Enforcement: manual code review + architecture-fitness lint on CI
(imports of `app.infrastructure` from `app.domain` fail the `lint` stage).

### 5.2 Ports / Adapters

Not applicable — `layered` does not require explicit ports/adapters.

## 6. Supporting patterns detail (Axis C detail)

None adopted.

## 7. Non-preferred shapes audit

Per `ARCHITECTURE_POLICY.md §9`.

| Flag | Triggered? | ADR |
|---|---|---|
| Layered internal structure for business app with ≥ 2 external adapters | NO (one adapter: SQLite) | n/a |
| Microservices without §6 evidence package | NO | n/a |
| Event-driven claim with < 3 event types | NO | n/a |
| AI-augmented without deterministic authority path | NO | n/a |
| Clean architecture for a CRUD prototype | NO | n/a |

## 8. Observability & testability expectations

| Aspect | Expectation |
|---|---|
| Unit-testable domain | `app/domain/counter.py` imports nothing from FastAPI or SQLite; runs under `pytest` standalone |
| Module / service boundary tests | Import lint on CI forbids `app.domain` importing `app.infrastructure` |
| Degradation path | `GET /health` returns 500 when DB unreachable; pipeline rollback on prod smoke failure |

## 9. Rewrite boundary awareness

None anticipated. The project is fixed-scope: a counter. Any feature
that forces a move from `layered` to `hexagonal` (e.g. a second adapter
like a message queue or external API) would constitute a rewrite
boundary — at which point the project likely loses its purpose as a
minimal validation harness.

## 10. Change Control

Changes to this profile require an ADR in `decision_log.md`,
`architect_agent` sign-off, and `governance_agent` acceptance at the
next go/no-go gate.
