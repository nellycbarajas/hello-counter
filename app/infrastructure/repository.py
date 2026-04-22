"""SQLite persistence for the single-row counter.

Uses sqlite3 from the standard library to minimize dependency surface.
Transaction boundary is one call — no concurrent-update concerns at this
scale, but we still use an ``UPDATE ... WHERE id=1`` predicate so a
second connection can't silently clobber.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path
from threading import Lock

_WRITE_LOCK = Lock()


class CounterRepository:
    def __init__(self, database_url: str):
        if not database_url.startswith("sqlite:///"):
            raise ValueError(f"Only sqlite:/// URLs are supported, got: {database_url}")
        self._db_path = database_url.removeprefix("sqlite:///")
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, isolation_level=None)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _ensure_schema(self) -> None:
        Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS counter (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    value INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                "INSERT OR IGNORE INTO counter (id, value) VALUES (1, 0)"
            )

    def get_value(self) -> int:
        with closing(self._connect()) as conn:
            row = conn.execute("SELECT value FROM counter WHERE id=1").fetchone()
            if not row:
                raise RuntimeError("Counter row missing; database not initialized.")
            return int(row[0])

    def increment(self, new_value: int, updated_at: str) -> None:
        with _WRITE_LOCK:
            with closing(self._connect()) as conn:
                cur = conn.execute(
                    "UPDATE counter SET value=?, updated_at=? WHERE id=1",
                    (new_value, updated_at),
                )
                if cur.rowcount != 1:
                    raise RuntimeError("Counter row missing; cannot increment.")

    def health_check(self) -> bool:
        try:
            with closing(self._connect()) as conn:
                conn.execute("SELECT 1").fetchone()
            return True
        except sqlite3.Error:
            return False
