# Project Brief — hello-counter

> **SEALED.** Do not edit inline. Record scope changes as ADRs in `decision_log.md`.
> Sealed on: 2026-04-22

## MVP Definition

### 1. Problem Statement

Teams validating the esencIA platform need a small but representative
project that exercises every phase — definition, architecture, devops,
governance, release — without drowning the validation in domain
complexity. Without such a harness, platform changes are validated only
against the two grandfathered pilots, which is slow and risky.

### 2. MVP Scope

**In scope (v1):**
- One persisted counter per environment
- HTTP POST `/increment` increments the counter, returns new value
- HTTP GET `/count` returns current value
- A single-page UI that shows the value and has a button to increment
- Sqlite persistence
- Docker-packaged, CI/CD through all 5 stages, deployed to `dev` / `staging` / `production`

**Out of scope (explicitly deferred):**
- Multi-user counters
- Authentication
- Rate limiting
- Analytics
- Multi-counter support
- Anything that introduces state beyond the single integer

### 3. Primary User Persona

**Name:** Platform operator
**Role:** Validates esencIA end-to-end
**Key goal:** Prove that every gate fires and every artifact exists in a fresh project
**Key frustration:** Validation projects that become real products and start accruing scope

### 4. Success Metrics

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| Time from `/new-project` to production deploy | n/a | ≤ 1 day | Platform-level observation |
| Failure-injection tests passing per `DEVOPS_VALIDATION_CHECKLIST.md §3` | 0 / 6 | 6 / 6 | Checklist sign-off |
| `/go-nogo` Architecture Gate + DevOps Gate — PASS | — | PASS | `governance_agent` verdict |

### 5. Value Proposition

A single command yields a running, governed, CI/CD-gated service. No
richer purpose.

---

## Discovery

### 1. User Segments

| Segment | Size / importance | Core need | Current workaround |
|---------|------------------|-----------|--------------------|
| Platform operators | Small, high importance | End-to-end validation of platform changes | Use the two grandfathered pilots, which have domain complexity that slows validation |

### 2. Existing Solutions & Gaps

| Solution | What it does | Why it falls short |
|----------|-------------|-------------------|
| Grandfathered pilots (RPE, intake) | Production projects | Domain complexity slows validation; cannot be broken on purpose |
| Ad-hoc toy repos | Small, fast | Not governed — no profiles, no gates, no alignment with policies |

### 3. Key Assumptions

- VALIDATED: A counter is the smallest domain that can still exercise the 5 pipeline stages.
- UNVALIDATED: A single integer is enough to exercise the Architecture Gate's `ai_augmented` rule. (It is not — this project does not adopt `ai_augmented`, which exercises the default path.)
- RISKY: Keeping the project truly minimal in face of later feature pressure. If a validation project accrues features, it stops being a validation project.

### 4. Biggest Unknowns

1. Do the two pipeline templates (`github-actions-base.yml`, `github-actions-serverless.yml`) generalize cleanly beyond this project?
2. How long does `devops_platform_agent` take to fill the pipeline for a new project?
3. Does `governance_agent`'s DevOps Gate catch all six failure modes declared in `DEVOPS_POLICY.md §7`?

### 5. Recommended Discovery Activities

Run `DEVOPS_VALIDATION_CHECKLIST.md` against this project end-to-end as
the first planned activity after deploy.

---

## UX Design

### 1. Core User Flows

**Flow 1: See counter**
1. User opens the URL
2. Page loads, fetches `GET /count`
3. Current value displayed in a large number
4. **Success state:** value rendered within 300 ms
5. **Failure state:** loading placeholder stays; toast shows "Counter unavailable"

**Flow 2: Increment counter**
1. User clicks the "+1" button
2. Button disables; spinner shown briefly
3. `POST /increment` returns new value
4. Number updates
5. **Success state:** number increments by 1
6. **Failure state:** toast shows error; button re-enables; number unchanged

### 2. Key Screens / Views

- **Counter view** — the only screen. Full-viewport centered counter, single primary button.

### 3. Critical Interactions

Loading: spinner while fetching. Error: toast with "Retry". Empty: never — counter starts at 0.

### 4. UI Copy

- Button: `+1`
- Error toast: `Counter unavailable — try again`
- Success toast: not shown (the number itself is the signal)

### 5. Accessibility Requirements

- WCAG AA target.
- Button reachable by keyboard; ARIA label `Increment counter`.
- Counter display has `aria-live="polite"` so screen readers announce updates.

---

## Data Model

### 1. Core Entities

```
Entity: Counter
Description: The single integer tracked by the service.
Key attributes:
  - id:     INTEGER (PK, always 1 — singleton)
  - value:  INTEGER (≥ 0)
  - updated_at: TIMESTAMP (ISO-8601)
Business rules:
  - There is exactly one row.
  - `value` monotonically increases; decrement is not supported.
```

### 2. Relationships

None. Single-row entity.

### 3. Domain Events

| Event | Trigger | Payload | Consumers |
|-------|---------|---------|-----------|
| CounterIncremented | POST /increment | `{ previous, new, at }` | Internal logger only |

### 4. Data Contracts (External APIs)

None — this service does not talk to external systems.

### 5. Privacy & Compliance Flags

- No PII.
- No consent required.
- Retention: indefinite (single row; negligible data).
