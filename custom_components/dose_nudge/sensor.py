"""Sensors.

Keep entities thin.
Business logic lives in MedicationManager.
UI should not contain scheduling maths. That way lies pain.
"""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .medication_manager import MedicationConfig

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        DoseNudgeNextDueSensor(entry, data),
        DoseNudgeRemainingSensor(entry, data),
    ])

class DoseNudgeBaseSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, data: dict) -> None:
        self._entry = entry
        self._data = data
        self._cfg = MedicationConfig(
            name=data["config"].get("name", "Medication"),
            interval_hours=int(data["config"].get("interval_hours", 8)),
        )
        self._med_id = data["config"].get("medication_id", "med")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Dose Nudge",
            "manufacturer": "TABARC-Code",
        }

class DoseNudgeNextDueSensor(DoseNudgeBaseSensor):
    _attr_name = "Next due"
    _attr_icon = "mdi:clock-outline"

    @property
    def native_value(self):
        mgr = self._data["manager"]
        dt = mgr.next_due(self._med_id, self._cfg)
        return dt.isoformat()

class DoseNudgeRemainingSensor(DoseNudgeBaseSensor):
    _attr_name = "Doses remaining"
    _attr_icon = "mdi:pill"

    @property
    def native_value(self):
        # Yeah, private. We'll tidy later if this grows.
        state = self._data["manager"]._state
        entry = state.get(str(self._med_id).strip().lower(), {})
        remaining = entry.get("doses_remaining")
        return remaining if isinstance(remaining, int) else None
