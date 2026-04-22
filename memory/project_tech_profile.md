# Technology Profile — hello-counter

> Aligned with `/esencIA/core/TECHNOLOGY_POLICY.md`. Filled during Phase 3.

## 1. Project Identification

| Field | Value |
|-------|-------|
| Project name | hello-counter |
| Slug | hello-counter |
| Owner (human — accountable) | platform |
| Tech lead (human — responsible) | platform |
| Created | 2026-04-22 |
| Profile version | `1.0` |
| Last updated | 2026-04-22 |

## 2. Technology Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Backend runtime | `Python 3.12 + FastAPI` | Match the two grandfathered pilots for operator context |
| Frontend runtime | `Vanilla HTML/JS/CSS` served by FastAPI static | No framework — the UI is a single button + counter display |
| Database | `SQLite` | Single-row singleton; stored as a named volume in Docker |
| API style | `REST` | POST /increment, GET /count, GET /health |
| Packaging | `Docker + docker-compose` | One image; compose for local spin-up |
| Deployment target | `Single-host Docker` in all three environments | Minimal validation footprint |

## 3. Classification

Per `TECHNOLOGY_POLICY.md §2`.

**Category:** General business system.

### Five-dimension justification

| Dimension | Value | Rationale |
|-----------|-------|-----------|
| Domain | CRUD-like | A counter is trivially simple state. |
| Data shape | Structured, single-row | No unstructured data, no large blobs. |
| Traffic | Low | Internal validation only. |
| Latency sensitivity | Low | Sub-second acceptable. |
| Regulatory | None | No PII, no financial data, no health data. |

Per `TECHNOLOGY_POLICY.md`: general business systems default to Node.js
+ TypeScript. **Deviation:** Python is used for operator-context
continuity with the grandfathered pilots. Recorded as ADR-001 in
`decision_log.md`. Accepted for this project because it is a
validation harness, not a business-facing system.

## 4. Non-functional requirements

| Requirement | Target |
|-------------|--------|
| Test coverage | ≥ 80% |
| p95 latency (increment) | < 200 ms |
| Recovery time on DB unavailability | Automatic (health endpoint signals degraded state) |

## 5. Approval Chain

| Role | Human |
|------|-------|
| Recommends | platform |
| Validates | platform |
| Approves | platform |

`governance_agent` verifies the chain at the go/no-go gate before any
release ships; a missing role blocks release.
