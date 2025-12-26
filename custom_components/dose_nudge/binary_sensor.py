"""Binary sensors.

These should be boring booleans.
Anything clever belongs in manager logic, not entity glue.
"""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .medication_manager import MedicationConfig

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DoseNudgeDueBinarySensor(entry, data)])

class DoseNudgeDueBinarySensor(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Dose due"
    _attr_icon = "mdi:alarm"

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

    @property
    def is_on(self):
        mgr = self._data["manager"]
        return mgr.is_due(self._med_id, self._cfg)
