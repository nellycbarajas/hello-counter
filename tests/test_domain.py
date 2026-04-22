"""Pure domain tests — no framework, no filesystem, no network."""

import datetime

import pytest

from app.domain.counter import increment, initial


def test_initial_returns_zero():
    state = initial()
    assert state.value == 0
    assert isinstance(state.updated_at, str)


def test_increment_increases_value():
    state = increment(0)
    assert state.value == 1


def test_increment_from_five():
    state = increment(5)
    assert state.value == 6


def test_increment_rejects_negative():
    with pytest.raises(ValueError):
        increment(-1)


def test_increment_accepts_now():
    fixed = datetime.datetime(2026, 4, 22, 10, 0, tzinfo=datetime.UTC)
    state = increment(7, now=fixed)
    assert state.value == 8
    assert state.updated_at == fixed.isoformat()
