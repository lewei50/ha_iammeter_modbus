from homeassistant.const import CONF_NAME, CONF_TYPE
from homeassistant.components.sensor import SensorEntity
import logging
from typing import Optional, Dict, Any

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
import homeassistant.util.dt as dt_util
from . import IamMeterModbusData

from .const import ATTR_MANUFACTURER, DOMAIN, SENSOR_TYPES, SENSOR_TYPES_3080, TYPE_3080, TYPE_3080T, IamMeterModbusSensorEntityDescription

_LOGGER = logging.getLogger(__name__)



async def async_setup_entry(hass, entry, async_add_entities):
    hub_name = entry.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]
    device_type = entry.data[CONF_TYPE]
    coordinator = hass.data[DOMAIN][entry.entry_id]
    device_info = {
        "identifiers": {(DOMAIN, hub_name)},
        "name": hub_name,
        "manufacturer": ATTR_MANUFACTURER,
    }

    entities = []
    if device_type == TYPE_3080T:
        for sensor_description in SENSOR_TYPES.values():
            sensor = IamMeterModbusSensor(
                coordinator,
                hub_name,
                hub,
                device_info,
                sensor_description,
            )
            entities.append(sensor)
    elif device_type == TYPE_3080:
        for sensor_description in SENSOR_TYPES_3080.values():
            sensor = IamMeterModbusSensor(
                coordinator,
                hub_name,
                hub,
                device_info,
                sensor_description,
            )
            entities.append(sensor)

    async_add_entities(entities)
    return True


class IamMeterModbusSensor(CoordinatorEntity, SensorEntity):
    """Representation of an IamMeter Modbus sensor."""

    def __init__(
        self,
        coordinator:IamMeterModbusData,
        platform_name,
        hub,
        device_info,
        description: IamMeterModbusSensorEntityDescription,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._platform_name = platform_name
        self._attr_device_info = device_info
        self._hub = hub
        self.entity_description: IamMeterModbusSensorEntityDescription = description

    @property
    def name(self):
        """Return the name."""
        return f"{self._platform_name} {self.entity_description.name}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{self._platform_name}_{self.entity_description.key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if(self.coordinator.data):
            return (
                self.coordinator.data.get(
                    self.entity_description.key, None
                )
            )
