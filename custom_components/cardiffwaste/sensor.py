"""Support for Cardiff Waste sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ALL_COLLECTIONS,
    ATTR_COLLECTION_TYPE,
    ATTR_IMAGE_URL,
    DEFAULT_OPTIONS,
    DOMAIN,
    TYPE_RECYCLING,
)
from .helpers import redact_uprn

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by Cardiff Council"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cardiff Waste sensor platform."""
    instance = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[SensorEntity] = []

    for collection in ALL_COLLECTIONS:
        if config_entry.options.get(collection, DEFAULT_OPTIONS[collection]):
            entities.append(CollectionSensor(instance, collection))

    async_add_entities(entities)


class CollectionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Cardiff Waste sensor."""

    def __init__(self, coordinator, collection_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        _LOGGER.debug(
            "Creating %s collection sensor for uprn: %s",
            collection_type,
            redact_uprn(coordinator.client.uprn),
        )
        self._data = coordinator
        self._type = collection_type
        self._name = (
            f"{collection_type.title()} Waste Collection"
            if collection_type is not TYPE_RECYCLING
            else f"{collection_type.title()} Collection"
        )
        self._id = f"cardiffwaste-{coordinator.client.uprn}-{collection_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the Unique ID of the sensor."""
        return self._id

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._type, {}).get("date")

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        """Return the device class of the sensor."""
        return SensorDeviceClass.DATE

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the state attributes of the sensor."""
        attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}

        _collection = self.coordinator.data.get(self._type, {})

        if _collection:
            attrs[ATTR_COLLECTION_TYPE] = _collection.get("type")
            attrs[ATTR_IMAGE_URL] = _collection.get("image")
        return attrs
