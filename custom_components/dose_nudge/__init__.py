"""Dose Nudge integration.

Nothing clever happens here.
Setup wires things together and keeps state alive across restarts.

If you want clever, build it on top. This stays boring.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .medication_manager import MedicationManager
from .store import DoseNudgeStore

PLATFORMS: list[str] = ["sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Load persisted state first. Restarts happen. Reality shouldn't rewind.
    store = DoseNudgeStore(hass)
    state = await store.async_load_state()

    manager = MedicationManager(state=state, store=store)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "store": store,
        "manager": manager,
        "config": dict(entry.data),
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unload_ok
