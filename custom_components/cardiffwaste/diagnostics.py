"""Diagnostics support for CardiffWaste."""

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import CardiffWasteData
from .const import CONF_UPRN, DOMAIN

TO_REDACT = {CONF_UPRN}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    instance: CardiffWasteData = hass.data[DOMAIN][entry.entry_id]

    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": instance.data,
        },
        TO_REDACT,
    )
