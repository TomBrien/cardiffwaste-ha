"""Config flow for Cardiff Waste integration."""
from __future__ import annotations

import logging
from typing import Any

from cardiffwaste import WasteCollections
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_UPRN, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_UPRN): str})


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Check we can get data for the property."""

    client = await hass.async_add_executor_job(WasteCollections, data[CONF_UPRN])

    if not client.check_valid_uprn():
        raise InvalidUPRN

    # Return info that you want to store in the config entry.
    return {"title": data[CONF_UPRN]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cardiff Waste."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        self._async_abort_entries_match({CONF_UPRN: user_input[CONF_UPRN]})

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except InvalidUPRN:
            errors["base"] = "invalid_uprn"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class InvalidUPRN(HomeAssistantError):
    """Error to indicate the address is not recognised."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
