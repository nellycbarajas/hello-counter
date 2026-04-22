# Decision Log — hello-counter

> Append-only ADR log. Every architectural or scope decision that is
> non-trivial is recorded here with status PROPOSED → ACCEPTED.

---

## ADR-001 — Technology Stack

- **Status:** ACCEPTED
- **Date:** 2026-04-22
- **Decided by:** architect_agent

**Context:** The project needs a minimal backend + frontend that can be
packaged as a single Docker image and exercised by the 5-stage CI/CD
pipeline.

**Decision:** FastAPI (Python 3.12) + SQLite for persistence + a
single-page vanilla HTML/JS/CSS frontend served by FastAPI as static
files.

**Alternatives rejected:**
- Node.js + Express + SQLite — equivalent outcome; Python chosen to
  match the two grandfathered pilots and keep operator context.
- Go + embedded BoltDB — adds runtime diversity the platform does not
  currently need.
- React/Next.js frontend — over-engineering for a single-button UI.

---

## ADR-002 — Internal Structure = `layered`

- **Status:** ACCEPTED
- **Date:** 2026-04-22
- **Decided by:** architect_agent

**Context:** `ARCHITECTURE_POLICY.md §4` rule B.2 prefers `hexagonal`
for business applications, but rule B.1 allows `layered` for
"Prototype or MVP under 6 weeks total effort, or team ≤ 2 engineers".

**Decision:** Adopt `layered` (Axis B). Under
`ARCHITECTURE_POLICY.md §4` rule B.1, this project is an MVP with a
one-engineer team and a one-week time box — B.1 fires.

**Alternatives rejected:** `hexagonal` — would be the preferred choice
for a business application with multiple adapters. This project has
one adapter (SQLite). The isolation cost is not justified.

---

## ADR-003 — Keep `staging` environment despite low stakes

- **Status:** ACCEPTED
- **Date:** 2026-04-22
- **Decided by:** devops_platform_agent

**Context:** `DEVOPS_POLICY.md §2` allows collapsing `dev` + `staging`
for low-stakes internal pilots via an ADR. This project qualifies for
that exception.

**Decision:** Keep `staging` as a distinct logical environment.

**Rationale:** The purpose of this project is to validate the pipeline
itself. Collapsing an environment reduces the surface under test.

---

## ADR-004 — No `ai_augmented` capability

- **Status:** ACCEPTED
- **Date:** 2026-04-22
- **Decided by:** architect_agent

**Context:** The Counter domain is entirely deterministic. There is no
reasoning, ranking, or generation that an LLM could augment.

**Decision:** Axis C = `[]`. The `ai_augmented` capability is not
adopted. This is the default; recorded here for auditability.

---

## ADR-005 — Health endpoint returns `{"status":"ok"}` with status 200

- **Status:** ACCEPTED
- **Date:** 2026-04-22
- **Decided by:** architect_agent

**Context:** The CI/CD pipeline's post-deploy smoke tests call a
health endpoint and expect 200. The rollback test in
`DEVOPS_VALIDATION_PLAN.md §4` depends on a predictable contract.

**Decision:** `GET /health` returns `{"status":"ok"}` with HTTP 200
whenever the database is reachable. It returns `{"status":"degraded"}`
with HTTP 500 when the database is unreachable.
