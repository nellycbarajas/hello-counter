"""FastAPI entry point. Wires HTTP routes to domain + repository."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import load_settings
from app.domain.counter import increment
from app.infrastructure.repository import CounterRepository

logger = logging.getLogger("hello-counter")
logging.basicConfig(level=logging.INFO)

settings = load_settings()
repo = CounterRepository(settings.database_url)

app = FastAPI(
    title="hello-counter",
    version=settings.version,
    description="Minimal counter service — esencIA validation harness.",
)


@app.get("/count")
def get_count() -> dict[str, int]:
    return {"value": repo.get_value()}


@app.post("/increment")
def post_increment() -> dict[str, int | str]:
    current = repo.get_value()
    next_state = increment(current)
    repo.increment(next_state.value, next_state.updated_at)
    logger.info("counter_incremented previous=%d new=%d", current, next_state.value)
    return {"value": next_state.value, "updated_at": next_state.updated_at}


@app.get("/health")
def health() -> JSONResponse:
    if repo.health_check():
        return JSONResponse({"status": "ok", "version": settings.version}, status_code=200)
    return JSONResponse({"status": "degraded", "version": settings.version}, status_code=500)


# ── Static frontend ─────────────────────────────────────────────────────
# Serve the single-page UI at "/" when the frontend dir exists. Kept
# mounted after routes so /count, /increment, /health take precedence.
_frontend_dir = Path(__file__).parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
