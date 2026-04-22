# Deploy — hello-counter

Single-service deployment; one Docker host per environment.

## First-time bring-up

```bash
docker compose up -d --build
docker compose logs -f hello-counter   # wait for "Uvicorn running"
curl -fsS http://127.0.0.1:8000/health
```

Expected response: `{"status":"ok","version":"local"}`.

## Everyday ops

| Task | Command |
|------|---------|
| Start / recover | `docker compose up -d` |
| Stop | `docker compose down` (keeps data volume) |
| Restart after config edit | `docker compose restart hello-counter` |
| Tail logs | `docker compose logs -f hello-counter` |
| Rebuild after code change | `docker compose up -d --build` |

## Environments

Each environment has its own docker-compose override and `.env.<env>`
file (bind-mounted, not in this repo):

- `dev`: `docker-compose.dev.yml + .env.dev`
- `staging`: `docker-compose.staging.yml + .env.staging`
- `production`: `docker-compose.prod.yml + .env.prod`

The CI/CD pipeline sets `IMAGE_TAG` and pulls from the registry; only
the tag changes between deploys.

## Backup / rollback

Data volume `counter-data` holds the SQLite file. To snapshot:

```bash
docker compose exec hello-counter sh -c \
  'sqlite3 /data/counter.db ".backup /tmp/backup.db"'
docker compose cp hello-counter:/tmp/backup.db ./backup-$(date -I).db
```

For application rollback, see `RUNBOOK.md §Rollback`.
