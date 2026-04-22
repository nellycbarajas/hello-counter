"""Pure counter logic. Framework-agnostic; no imports from FastAPI or sqlite.

Architecture-fitness check (lint stage) verifies this module never imports
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class CounterState:
    value: int
    updated_at: str


def increment(
    current: int,
    now: datetime.datetime | None = None,
) -> CounterState:
    if current < 0:
        raise ValueError("Counter value must be non-negative.")
    new_value = current + 1
    ts = (now or datetime.datetime.now(datetime.timezone.utc)).isoformat()
    return CounterState(value=new_value, updated_at=ts)


def initial() -> CounterState:
    return CounterState(
        value=0,
        updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )