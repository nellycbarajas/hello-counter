# DevOps Profile — hello-counter

> Aligned with `/esencIA/core/DEVOPS_POLICY.md`. Filled during Phase 3.

## 1. Project Identification

| Field | Value |
|-------|-------|
| Project name | hello-counter |
| Slug | hello-counter |
| Owner (human — accountable) | platform |
| DevOps lead (human — responsible) | platform |
| Created | 2026-04-22 |
| Profile version | `1.0` |
| Last updated | 2026-04-22 |

## 2. CI/CD Platform

- [x] GitHub Actions _(preferred)_

## 3. Environments

| Env | Host / platform | Config source | Data source | Deploy trigger |
|-----|-----------------|---------------|-------------|----------------|
| `dev` | Single Docker host (dev VM) | `.env.dev` | SQLite volume `counter-dev` | Auto on merge to `main` |
| `staging` | Single Docker host (staging VM) | `.env.staging` | SQLite volume `counter-staging` | Auto after `dev` smoke green |
| `production` | Single Docker host (prod VM) | `.env.prod` | SQLite volume `counter-prod` | Manual, after `/go-nogo` = GO |

**Environment collapse:** NO. ADR-003 keeps `staging` distinct to
exercise the full pipeline during validation.

## 4. Branching Strategy

- [x] Trunk-based (default)

Branch-protection rules on `main`:
- [x] No direct pushes
- [x] PR requires CI green before merge
- [x] PR requires at least one reviewer
- [x] Force-push disabled
- [x] Branch deletion disabled

## 5. Pipeline Stages

| Stage | Tool / command | Coverage / threshold | Failure action |
|-------|----------------|----------------------|----------------|
| `build` | `docker build -t hello-counter:$IMAGE_TAG .` | Lockfile integrity via `pip install -r requirements.txt` with `--no-deps` check | Block PR |
| `lint` | `ruff check .` + `mypy app/` + architecture-fitness check (forbid `app.domain` importing `app.infrastructure`) | 0 errors | Block PR |
| `test` | `pytest -q --cov=app --cov-report=xml` | ≥ 80% | Block PR |
| `security` | `pip-audit --strict` + `gitleaks detect` + `trivy image` | 0 HIGH+ | Block PR |
| `package` | Tag and push image to registry | Image built and pushed | Block PR |

Optional stages: none.

## 6. Release Strategy

| Environment | Approval | Strategy |
|-------------|----------|----------|
| `dev` | None (automated) | Replace — `docker compose up -d --build` |
| `staging` | None (automated, after dev green) | Replace |
| `production` | **Manual** — required reviewer in GH Environment | Replace with previous-tag rollback on smoke failure |

Rollback procedure: see `RUNBOOK.md §Rollback`.

## 7. Secrets and Configuration

| Category | Storage |
|----------|---------|
| Secrets (registry token, SSH deploy key) | GitHub Encrypted Secrets (`REGISTRY_TOKEN`, `DEPLOY_SSH_KEY`) |
| Environment-specific config | `.env.<env>` files bind-mounted at deploy time (not in repo) |
| Compile-time config | `app/config.py` — reads env vars with defaults |

Confirmed: no secret committed to source control.

## 8. Observability and Post-Deploy

| Concern | Expectation |
|---------|-------------|
| Deploy marker | Every deploy appends a line to `/var/log/hello-counter.deploy.log` with version tag and timestamp |
| Smoke test | `curl -fsS http://<host>/health` within 60s of deploy; failure triggers rollback |
| Metrics | None (out of scope for the minimum validation project) |
| Alerts | None (out of scope) |

## 9. DevOps Gate readiness (§7 of policy)

| Check | Status |
|-------|--------|
| Pipeline file committed to repo (`.github/workflows/ci-cd.yml`) | YES |
| All 5 mandatory stages present | YES |
| Last green build on `main` is ≤ 7 days old | _TBD — set after first merge_ |
| No open HIGH+ security findings | YES |
| Rollback procedure documented in `RUNBOOK.md` | YES |
| `dev` + `staging` deploys of this release green | _TBD — set after first deploy_ |

## 10. Change Control

Changes to this profile require an ADR in `decision_log.md`,
`devops_platform_agent` ownership, and `governance_agent` acceptance
at the next go/no-go gate.
