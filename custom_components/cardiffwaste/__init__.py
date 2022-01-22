"""The Cardiff Waste integration."""
from __future__ import annotations

from datetime import timedelta

from cardiffwaste import WasteCollections

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.util import Throttle

from .const import CONF_UPRN, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cardiff Waste from a config entry."""

    instance = await hass.async_add_executor_job(create_and_update_instance, entry)

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


def create_and_update_instance(entry: ConfigEntry) -> CardiffWasteData:
    """Create and update a Cardiff Waste Data instance."""
    client = WasteCollections(entry.data[CONF_UPRN])
    instance = CardiffWasteData(client)
    instance.update()
    return instance


async def update_listener(hass, config_entry):
    """Handle options update."""

    await hass.config_entries.async_reload(config_entry.entry_id)

    registry = entity_registry.async_get(hass)
    entities = entity_registry.async_entries_for_config_entry(
        registry, config_entry.entry_id
    )

    # Remove orphaned entities
    for entity in entities:
        collection_type = entity.unique_id.split("-")[-1]
        if not config_entry.options.get(collection_type):
            registry.async_remove(entity.entity_id)


class CardiffWasteData:
    """Get the latest data and update the states."""

    def __init__(self, client: WasteCollections) -> None:
        """Init the waste data object."""

        self.client = client
        self.collections: dict | None = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from Cardiff Waste."""

        self.collections = self.client.get_next_collections()
