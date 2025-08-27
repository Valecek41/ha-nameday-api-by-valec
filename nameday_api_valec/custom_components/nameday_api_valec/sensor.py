from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Nameday sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        NamedaySensor(coordinator, "today"),
        NamedaySensor(coordinator, "tomorrow")
    ], True)


class NamedaySensor(SensorEntity):
    """Representation of a Nameday sensor."""

    def __init__(self, coordinator, which):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.which = which  # "today" or "tomorrow"
        self._attr_name = f"Nameday {which.capitalize()}"
        self._attr_unique_id = f"nameday_{which}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.which)

    async def async_update(self):
        """Fetch new state data from the coordinator."""
        await self.coordinator.async_request_refresh()
