"""Persistence layer.

Home Assistant restarts. Power cuts happen. People update.
If we don't persist, reminders will reappear and nobody will trust this thing.

Store is local-only and HA-native. No extra databases. No drama.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY, STORAGE_VERSION

class DoseNudgeStore:
    def __init__(self, hass: HomeAssistant) -> None:
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)

    async def async_load_state(self) -> dict:
        data = await self._store.async_load()
        return data if isinstance(data, dict) else {}

    async def async_save_state(self, state: dict) -> None:
        # Yes, we save the whole dict.
        # It's small and predictable. I'd rather have boring correctness than clever partial updates.
        await self._store.async_save(state)
