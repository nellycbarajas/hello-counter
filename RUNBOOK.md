# Runbook — hello-counter

On-call runbook. Intended reader: operator paged at 3 AM.

## Service summary

- One FastAPI container per environment.
- SQLite on a named Docker volume (`counter-data`).
- No external dependencies.

## Health check

```
curl -fsS https://<env-host>/health
```

Expected: HTTP 200, body `{"status":"ok", ...}`.

## Known failures and recovery

| Symptom | Likely cause | Recovery |
|---------|--------------|----------|
| `/health` returns 500 `{"status":"degraded"}` | SQLite file corrupt or permissions wrong on `/data` | Stop service, restore latest backup (`DEPLOY.md §Backup`), restart |
| Frontend blank page | Static files missing from image | Rebuild image (`docker compose up -d --build`); confirm `COPY frontend /app/frontend` in Dockerfile |
| `/increment` returns 500 but `/count` works | Write lock contention or disk full | Check `docker system df` and `docker compose logs`; free disk or restart |
| Pipeline deploys new tag but service still on old image | Pull failed silently | `docker compose pull && docker compose up -d` |

## Rollback

**Pre-requisite:** the previous production image tag is recorded in
`/opt/hello-counter/.previous_tag` on the production host (written by
the successful prior deploy step).

Manual rollback on the production host:

```bash
ssh prod-host
PREVIOUS=$(cat /opt/hello-counter/.previous_tag)
docker pull ghcr.io/<owner>/hello-counter:$PREVIOUS
IMAGE_TAG=$PREVIOUS docker compose -f /opt/hello-counter/docker-compose.yml up -d
curl -fsS http://127.0.0.1:8000/health    # must return 200
```

Record an ADR in `memory/decision_log.md` titled `Rollback — release/r<N>
— <brief cause>` immediately after.

## Post-deploy verification

After any deploy:

1. `curl -fsS https://<env-host>/health` returns 200.
2. `curl -fsS https://<env-host>/count` returns a JSON body with a `value` key.
3. `curl -fsS -X POST https://<env-host>/increment` returns `value` incremented by 1.
4. UI loads at `https://<env-host>/` and the counter number renders.

## Escalation

On-call rota: _TBD_ (this is a validation harness; real rota defined
per org).
