"""The Iammeter Modbus Integration."""
import asyncio
import logging
import threading
import async_timeout
from datetime import timedelta
from typing import Optional
from requests.exceptions import Timeout

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL, CONF_TYPE
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder

from .const import (
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TYPE,
    DOMAIN,
    TYPE_3080,
    TYPE_3080T,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER_MODBUS_LIB = logging.getLogger("pymodbus.logging")
_LOGGER_MODBUS_LIB.setLevel(logging.CRITICAL)

IAMMETER_MODBUS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.string,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): cv.positive_int,
        vol.Required(CONF_TYPE, default=DEFAULT_TYPE):vol.In([TYPE_3080, TYPE_3080T]),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: IAMMETER_MODBUS_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor"]
SCAN_INTERVAL = timedelta(seconds=4)


async def async_setup(hass, config):
    """Set up the IamMeter modbus component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    _LOGGER.info("async_setup_entry")
    """Set up a IamMeter mobus."""
    host = entry.data[CONF_HOST]
    type = entry.data[CONF_TYPE]
    name = entry.data[CONF_NAME]
    port = entry.data[CONF_PORT]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]

    _LOGGER.debug("Setup %s.%s", DOMAIN, name)

    hub = IammeterModbusHub(hass, name, host, port, scan_interval, type)
    """Register the hub."""
    hass.data[DOMAIN][name] = {"hub": hub}
    
    coordinator = IamMeterModbusData(hass, hub)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await coordinator.async_config_entry_first_refresh()

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True

async def async_unload_entry(hass, entry):
    """Unload IamMeter mobus entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False

    hass.data[DOMAIN].pop(entry.data[CONF_NAME])
    return True

class IamMeterModbusData(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, my_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="IamMeterModbus Data",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=3),
        )
        self.my_api = my_api

    async def _async_update_data(self):
        #Fetch data from API endpoint.
        return await self.my_api.async_refresh_modbus_data()

class IammeterModbusHub:
    """Thread safe wrapper class for pymodbus."""

    def __init__(
        self,
        hass,
        name,
        host,
        port,
        scan_interval,
        type,
    ):
        """Initialize the Modbus hub."""
        self._hass = hass
        self._client = ModbusTcpClient(host=host, port=port, timeout=2)
        self._value_attr_name = "count"
        self._lock = threading.Lock()
        self._name = name
        self._type = type
        self._scan_interval = timedelta(seconds=scan_interval)
        self._unsub_interval_method = None
        self._sensors = []
        self.data = {}

    async def async_refresh_modbus_data(self, _now: Optional[int] = None):
        """Time to update."""
        self.connect()
        
        try:
            async with async_timeout.timeout(2):
                update_result = self.read_modbus_data()
                if update_result:
                    return self.data
        except (OSError, Timeout) as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    @property
    def name(self):
        """Return the name of this hub."""
        return self._name

    def close(self):
        """Disconnect client."""
        with self._lock:
            self._client.close()

    def connect(self):
        """Connect client."""
        with self._lock:
            if self._client.connected is None:
                self._client.connect()

    def read_holding_registers(self, unit, address, count):
        """Read holding registers."""
        with self._lock:
            kwargs = {"slave": unit} if unit else {}
            # return self._client.read_holding_registers(address, count, **kwargs)
            kwargs[self._value_attr_name] = count
            return self._client.read_holding_registers(address, **kwargs)
        
    def read_modbus_data(self):
        try:
            return self.read_modbus_holding_registers()
        except ConnectionException as ex:
            #_LOGGER.error("Reading data failed! IamMeter is offline.")
            raise UpdateFailed(f"Error communicating with API: {ex}")

    def read_modbus_holding_registers(self):
        typeCount = 38
        if self._type == TYPE_3080:
            typeCount = 8
        inverter_data = self.read_holding_registers(unit=1, address=0x0, count=typeCount)

        if inverter_data.isError():
            return False

        decoder = BinaryPayloadDecoder.fromRegisters(
            inverter_data.registers, byteorder=Endian.BIG
        )

        if self._type == TYPE_3080:
            voltage_a = decoder.decode_16bit_uint()
            self.data["voltage_a"] = round(voltage_a * 0.01, 1)

            current_a = decoder.decode_16bit_uint()
            self.data["current_a"] = round(current_a * 0.01, 1)

            power_a = decoder.decode_32bit_int()
            self.data["power_a"] = power_a

            import_energy_a = decoder.decode_32bit_uint()
            self.data["import_energy_a"] = round(import_energy_a * 0.0003125, 3)

            export_energy_a = decoder.decode_32bit_uint()
            self.data["export_energy_a"] = round(export_energy_a * 0.0003125, 3)

            return True
        else:
            voltage_a = decoder.decode_16bit_uint()
            self.data["voltage_a"] = round(voltage_a * 0.01, 1)

            current_a = decoder.decode_16bit_uint()
            self.data["current_a"] = round(current_a * 0.01, 1)

            power_a = decoder.decode_32bit_int()
            self.data["power_a"] = power_a

            import_energy_a = decoder.decode_32bit_uint()
            self.data["import_energy_a"] = round(import_energy_a * 0.00125, 2)

            export_energy_a = decoder.decode_32bit_uint()
            self.data["export_energy_a"] = round(export_energy_a * 0.00125, 2)

            power_factor_a = decoder.decode_16bit_uint()
            self.data["power_factor_a"] = round(power_factor_a * 0.001, 2)

            decoder.skip_bytes(2)

            voltage_b = decoder.decode_16bit_uint()
            self.data["voltage_b"] = round(voltage_b * 0.01, 1)

            current_b = decoder.decode_16bit_uint()
            self.data["current_b"] = round(current_b * 0.01, 1)

            power_b = decoder.decode_32bit_int()
            self.data["power_b"] = power_b

            import_energy_b = decoder.decode_32bit_uint()
            self.data["import_energy_b"] = round(import_energy_b * 0.00125, 2)

            export_energy_b = decoder.decode_32bit_uint()
            self.data["export_energy_b"] = round(export_energy_b * 0.00125, 2)

            power_factor_b = decoder.decode_16bit_uint()
            self.data["power_factor_b"] = round(power_factor_b * 0.001, 2)

            decoder.skip_bytes(2)

            voltage_c = decoder.decode_16bit_uint()
            self.data["voltage_c"] = round(voltage_c * 0.01, 1)

            current_c = decoder.decode_16bit_uint()
            self.data["current_c"] = round(current_c * 0.01, 1)

            power_c = decoder.decode_32bit_int()
            self.data["power_c"] = power_c

            import_energy_c = decoder.decode_32bit_uint()
            self.data["import_energy_c"] = round(import_energy_c * 0.00125, 2)

            export_energy_c = decoder.decode_32bit_uint()
            self.data["export_energy_c"] = round(export_energy_c * 0.00125, 2)

            power_factor_c = decoder.decode_16bit_uint()
            self.data["power_factor_c"] = round(power_factor_c * 0.001, 2)

            decoder.skip_bytes(2)

            frequency = decoder.decode_16bit_uint()
            self.data["frequency"] = round(frequency * 0.01, 1)

            decoder.skip_bytes(2)

            total_power = decoder.decode_32bit_int()
            self.data["total_power"] = total_power

            total_import_energy = decoder.decode_32bit_uint()
            self.data["total_import_energy"] = round(total_import_energy * 0.00125, 2)

            total_export_energy = decoder.decode_32bit_uint()
            self.data["total_export_energy"] = round(total_export_energy * 0.00125, 2)

            return True
