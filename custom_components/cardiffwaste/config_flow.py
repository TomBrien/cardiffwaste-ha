"""Config flow for Cardiff Waste integration."""
from __future__ import annotations

import logging
from typing import Any

from cardiffwaste import WasteCollections
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_UPRN,
    DEFAULT_OPTIONS,
    DOMAIN,
    TYPE_FOOD,
    TYPE_GARDEN,
    TYPE_GENERAL,
    TYPE_HYGIENE,
    TYPE_RECYCLING,
)
from .helpers import redact_uprn

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_UPRN): str})


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Check we can get data for the property."""

    _LOGGER.debug("Validating uprn: %s", redact_uprn(data[CONF_UPRN]))

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
            _LOGGER.debug("uprn: %s is invalid", redact_uprn(user_input[CONF_UPRN]))
            errors["base"] = "invalid_uprn"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(
                title=info["title"], data=user_input, options=DEFAULT_OPTIONS
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Cardiff Waste."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""

        errors = {}

        default_food = self.config_entry.options.get(TYPE_FOOD, True)
        default_garden = self.config_entry.options.get(TYPE_GARDEN, True)
        default_general = self.config_entry.options.get(TYPE_GENERAL, True)
        default_hygiene = self.config_entry.options.get(TYPE_HYGIENE, False)
        default_recycling = self.config_entry.options.get(TYPE_RECYCLING, True)

        if user_input is not None:

            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        TYPE_FOOD,
                        default=default_food,
                    ): bool,
                    vol.Optional(
                        TYPE_GARDEN,
                        default=default_garden,
                    ): bool,
                    vol.Optional(
                        TYPE_GENERAL,
                        default=default_general,
                    ): bool,
                    vol.Optional(
                        TYPE_HYGIENE,
                        default=default_hygiene,
                    ): bool,
                    vol.Optional(
                        TYPE_RECYCLING,
                        default=default_recycling,
                    ): bool,
                }
            ),
            errors=errors,
        )


class InvalidUPRN(HomeAssistantError):
    """Error to indicate the address is not recognised."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
