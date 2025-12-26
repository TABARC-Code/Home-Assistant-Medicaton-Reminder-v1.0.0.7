"""Core scheduling and state.

All time handling lives here.
If DST breaks something, it should break in ONE place.

This is not a medical device. It's a reminder engine.
It should be predictable and hard to accidentally corrupt.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.util import dt as dt_util

@dataclass(frozen=True)
class MedicationConfig:
    name: str
    interval_hours: int = 8
    doses_total: int | None = None  # optional, for "remaining" tracking

class MedicationManager:
    def __init__(self, state: dict[str, Any], store) -> None:
        self._state: dict[str, Any] = state or {}
        self._store = store

    def _med_key(self, med_id: str) -> str:
        return str(med_id).strip().lower()

    def is_due(self, med_id: str, cfg: MedicationConfig) -> bool:
        key = self._med_key(med_id)
        last_taken = self._state.get(key, {}).get("last_taken")
        now = dt_util.now()

        if not last_taken:
            # Never taken -> treat as due. Simple. Predictable.
            return True

        last_dt = dt_util.parse_datetime(last_taken)
        if last_dt is None:
            return True

        return now >= (last_dt + timedelta(hours=int(cfg.interval_hours)))

    def next_due(self, med_id: str, cfg: MedicationConfig):
        key = self._med_key(med_id)
        last_taken = self._state.get(key, {}).get("last_taken")
        now = dt_util.now()

        if not last_taken:
            return now

        last_dt = dt_util.parse_datetime(last_taken)
        if last_dt is None:
            return now

        return last_dt + timedelta(hours=int(cfg.interval_hours))

    async def mark_taken(self, med_id: str) -> bool:
        # Idempotent on purpose. Buttons get double-tapped. Automations loop.
        key = self._med_key(med_id)
        entry = self._state.setdefault(key, {})

        last_taken = entry.get("last_taken")
        if last_taken:
            last_dt = dt_util.parse_datetime(last_taken)
            if last_dt is not None and (dt_util.now() - last_dt) < timedelta(seconds=5):
                return False

        entry["last_taken"] = dt_util.now().isoformat()

        remaining = entry.get("doses_remaining")
        if isinstance(remaining, int) and remaining > 0:
            entry["doses_remaining"] = remaining - 1

        await self._store.async_save_state(self._state)
        return True

    async def refill(self, med_id: str, amount: int) -> bool:
        key = self._med_key(med_id)
        if amount <= 0:
            return False

        entry = self._state.setdefault(key, {})
        remaining = entry.get("doses_remaining")

        if remaining is None:
            entry["doses_remaining"] = amount
        elif isinstance(remaining, int):
            entry["doses_remaining"] = max(0, remaining + amount)
        else:
            entry["doses_remaining"] = amount

        await self._store.async_save_state(self._state)
        return True
