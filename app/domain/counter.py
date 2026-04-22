"""Pure counter logic. Framework-agnostic; no imports from FastAPI or sqlite.

Architecture-fitness check (lint stage) verifies this module never imports
from ``app.infrastructure``. See project_architecture_profile.md §5.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import cast


@dataclass(frozen=True)
class CounterState:
    value: int
    updated_at: str


def increment(current: int, now: datetime | None = None) -> CounterState:
    if current < 0:
        raise ValueError("Counter value must be non-negative.")
    new_value = current + 1
    ts = (now or datetime.now(cast(datetime, datetime).UTC)).isoformat()
    return CounterState(value=new_value, updated_at=ts)


def initial() -> CounterState:
    return CounterState(value=0, updated_at=datetime.now(cast(datetime, datetime).UTC).isoformat())
