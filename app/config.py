"""Environment-driven configuration. Defaults target local dev."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    environment: str
    version: str


def load_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("DATABASE_URL", "sqlite:///./counter.db"),
        environment=os.environ.get("ENVIRONMENT", "dev"),
        version=os.environ.get("APP_VERSION", "dev"),
    )
