"""Config flow.

UI setup because YAML-only integrations tend to become archaeology projects.
This is minimal on purpose. Add options later once it's stable.
"""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

STEP_USER_SCHEMA = vol.Schema({
    vol.Required("medication_id", default="morning_med"): str,
    vol.Required("name", default="Medication"): str,
    vol.Required("interval_hours", default=8): vol.All(int, vol.Range(min=1, max=72)),
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_SCHEMA)

        title = user_input.get("name") or "Dose Nudge"
        return self.async_create_entry(title=title, data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        # TODO: add snooze windows, quiet hours, multiple meds.
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
