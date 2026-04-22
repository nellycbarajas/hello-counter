"""Pure domain tests — no framework, no filesystem, no network."""

from datetime import datetime, timezone

import pytest

from app.domain.counter import increment, initial


def test_initial_value_is_zero():
    state = initial()
    assert state.value == 0
    assert state.updated_at  # ISO-8601 string


def test_increment_raises_on_negative():
    with pytest.raises(ValueError):
        increment(-1)


def test_increment_by_one():
    state = increment(5)
    assert state.value == 6


def test_increment_is_monotonic():
    s1 = increment(0)
    s2 = increment(s1.value)
    assert s2.value == 2


def test_increment_accepts_now():
    fixed = datetime(2026, 4, 22, 10, 0, tzinfo=datetime.UTC) 
    state = increment(7, now=fixed)
    assert state.value == 8
    assert state.updated_at == fixed.isoformat()
