"""Support for Cardiff Waste sensors."""
from __future__ import annotations

import logging

from custom_components.cardiffwaste.helpers import redact_uprn
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ALL_COLLECTIONS,
    ATTR_COLLECTION_TYPE,
    ATTR_IMAGE_URL,
    DEFAULT_OPTIONS,
    DOMAIN,
<<<<<<< HEAD
=======
    TYPE_FOOD,
    TYPE_GARDEN,
    TYPE_GENERAL,
    TYPE_HYGIENE,
>>>>>>> Support hygiene waste collections (#6)
    TYPE_RECYCLING,
)

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


class CollectionSensor(SensorEntity):
    """Representation of a Cardiff Waste sensor."""

    def __init__(self, collection_data, collection_type):
        """Initialize the sensor."""
        _LOGGER.debug(
            "Creating %s collection sensor for uprn: %s",
            collection_type,
            redact_uprn(collection_data.client.uprn),
        )
        self._data = collection_data
        self._type = collection_type
        self._name = (
            f"{collection_type.title()} Waste Collection"
            if collection_type is not TYPE_RECYCLING
            else f"{collection_type.title()} Collection"
        )
        self._id = f"cardiffwaste-{collection_data.client.uprn}-{collection_type}"

        self._collection = self._data.collections.get(collection_type, {})

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
        return self._collection.get("date")

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        """Return the device class of the sensor."""
        return SensorDeviceClass.DATE

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the state attributes of the sensor."""
        attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}
        if self._collection:
            attrs[ATTR_COLLECTION_TYPE] = self._collection.get("type")
            attrs[ATTR_IMAGE_URL] = self._collection.get("image")
        return attrs

    def update(self):
        """Get the latest state of the sensor."""

        _LOGGER.debug(
            "Updating %s collection sensor for uprn: %s",
            self._type,
            redact_uprn(self._data.client.uprn),
        )

        self._data.update()

        self._collection = self._data.collections.get(self._type, {})
