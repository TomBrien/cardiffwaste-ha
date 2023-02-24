"""Constants for the Cardiff Waste integration."""

DOMAIN = "cardiffwaste"

ATTR_COLLECTION_TYPE = "collection_type"
ATTR_IMAGE_URL = "image_URL"

CONF_ADDRESS_PICKER = "address_picker"
CONF_POST_CODE = "post_code"
CONF_UPRN = "uprn"

TYPE_CHRISTMAS_TREE = "christmas tree"
TYPE_FOOD = "food"
TYPE_GARDEN = "garden"
TYPE_GENERAL = "general"
TYPE_GLASS = "glass"
TYPE_HYGIENE = "hygiene"
TYPE_RECYCLING = "recycling"


ALL_COLLECTIONS = [
    TYPE_CHRISTMAS_TREE,
    TYPE_GARDEN,
    TYPE_GENERAL,
    TYPE_GLASS,
    TYPE_FOOD,
    TYPE_HYGIENE,
    TYPE_RECYCLING,
]

DEFAULT_OPTIONS = {
    TYPE_CHRISTMAS_TREE: True,
    TYPE_FOOD: True,
    TYPE_GARDEN: True,
    TYPE_GENERAL: True,
    TYPE_GLASS: False,
    TYPE_HYGIENE: False,
    TYPE_RECYCLING: True,
}
