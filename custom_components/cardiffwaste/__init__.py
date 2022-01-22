"""The Cardiff Waste integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from cardiffwaste import WasteCollections

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import Throttle

from .const import CONF_UPRN, DOMAIN
from .helpers import redact_uprn

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [Platform.SENSOR]

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cardiff Waste from a config entry."""

    _LOGGER.debug("Setting up entry for uprn: %s", redact_uprn(entry.data[CONF_UPRN]))

    instance = await create_and_update_instance(hass, entry)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = instance
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def create_and_update_instance(hass, entry: ConfigEntry) -> CardiffWasteData:
    """Create and update a Cardiff Waste Data instance."""
    _LOGGER.debug(
        "Registering instance for uprn: %s", redact_uprn(entry.data[CONF_UPRN])
    )
    client = await hass.async_add_executor_job(WasteCollections, entry.data[CONF_UPRN])
    instance = CardiffWasteData(hass, client)
    _LOGGER.debug(
        "Requesting instance update for uprn: %s", redact_uprn(entry.data[CONF_UPRN])
    )
    await instance.async_config_entry_first_refresh()

    return instance


async def update_listener(hass, entry):
    """Handle options update."""

    _LOGGER.debug(
        "Handling options change for uprn: %s", redact_uprn(entry.data[CONF_UPRN])
    )

    await hass.config_entries.async_reload(entry.entry_id)

    registry = entity_registry.async_get(hass)
    entities = entity_registry.async_entries_for_config_entry(registry, entry.entry_id)

    # Remove orphaned entities
    for entity in entities:
        collection_type = entity.unique_id.split("-")[-1]
        if not entry.options.get(collection_type):
            _LOGGER.debug(
                "Removing %s collection for uprn: %s",
                collection_type,
                redact_uprn(entry.data[CONF_UPRN]),
            )
            registry.async_remove(entity.entity_id)


class CardiffWasteData(DataUpdateCoordinator):
    """Get the latest data and update the states."""

    def __init__(self, hass, client: WasteCollections) -> None:
        """Init the waste data object."""

        self._hass = hass
        self.client = client

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=MIN_TIME_BETWEEN_UPDATES
        )

    async def _async_update_data(self):
        """Get the latest data from Cardiff Waste."""
        _LOGGER.debug(
            "Allowing instance update for uprn: %s", redact_uprn(self.client.uprn)
        )
        return await self._hass.async_add_executor_job(self.client.get_next_collections)
