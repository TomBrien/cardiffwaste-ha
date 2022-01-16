"""Support for Cardiff Waste sensors."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_COLLECTION_TYPE,
    ATTR_IMAGE_URL,
    DOMAIN,
    TYPE_FOOD,
    TYPE_GARDEN,
    TYPE_GENERAL,
    TYPE_RECYCLING,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by Cardiff Council"

COLLECTIONS = [TYPE_FOOD, TYPE_GARDEN, TYPE_GENERAL, TYPE_RECYCLING]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cardiff Waste sensor platform."""
    instance = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[SensorEntity] = []

    for collection in COLLECTIONS:
        entities.append(CollectionSensor(instance, collection))

    async_add_entities(entities)


class CollectionSensor(SensorEntity):
    """Representation of a Cardiff Waste sensor."""

    def __init__(self, collection_data, collection_type):
        """Initialize the sensor."""
        self._data = collection_data
        self._type = collection_type
        self._name = (
            f"{collection_type.title()} Waste Collection"
            if collection_type is not TYPE_RECYCLING
            else f"{collection_type.title()} Collection"
        )
        self._id = f"cardiffwaste-{collection_type}"

        if collection_type is TYPE_FOOD:
            self._collection = collection_data.collections.food
        elif collection_type is TYPE_GARDEN:
            self._collection = collection_data.collections.garden
        elif collection_type is TYPE_GENERAL:
            self._collection = collection_data.collections.general
        elif collection_type is TYPE_RECYCLING:
            self._collection = collection_data.collections.recycling
        self._state = (
            self._collection.collection_date if self._collection.loaded else None
        )

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
        return self._state

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        """Return the device class of the sensor."""
        return SensorDeviceClass.DATE

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}
        if self._collection.loaded:
            attrs[ATTR_COLLECTION_TYPE] = self._collection.collection_type
            attrs[ATTR_IMAGE_URL] = self._collection.image
        return attrs

    def update(self):
        """Get the latest state of the sensor."""
        self._data.update()
        if self._type is TYPE_FOOD:
            self._collection = self._data.collections.food
        elif self._type is TYPE_GARDEN:
            self._collection = self._data.collections.garden
        elif self._type is TYPE_GENERAL:
            self._collection = self._data.collections.general
        elif self._type is TYPE_RECYCLING:
            self._collection = self._data.collections.recycling
        self._state = (
            self._collection.collection_date if self._collection.loaded else None
        )
