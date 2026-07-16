"""The Iammeter Modbus Integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SCAN_INTERVAL, CONF_TYPE
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusException

from .const import (
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TYPE,
    DOMAIN,
    MAX_OFFLINE_RETRY_INTERVAL,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    OFFLINE_RETRY_INTERVAL,
    SUPPORTED_TYPES,
    TYPE_2067,
    TYPE_3080,
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
        ): vol.All(
            cv.positive_int,
            vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
        ),
        vol.Required(CONF_TYPE, default=DEFAULT_TYPE): vol.In(SUPPORTED_TYPES),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: IAMMETER_MODBUS_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor"]


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
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    _LOGGER.debug("Setup %s.%s", DOMAIN, name)

    hub = IammeterModbusHub(name, host, port, type)
    coordinator = IamMeterModbusData(hass, hub, scan_interval)
    hass.data[DOMAIN][entry.entry_id] = coordinator
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        hub.close()
        hass.data[DOMAIN].pop(entry.entry_id, None)
        raise

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    """Unload IamMeter mobus entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(
                    entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False

    coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
    if coordinator is not None:
        await coordinator.async_shutdown()
    return True


class IamMeterModbusData(DataUpdateCoordinator):
    """Coordinate polling and offline retry intervals."""

    def __init__(self, hass, my_api, scan_interval):
        """Initialize my coordinator."""
        self.my_api = my_api
        self._normal_update_interval = timedelta(seconds=scan_interval)
        self._consecutive_failures = 0
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="IamMeterModbus Data",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=self._normal_update_interval,
        )

    async def _async_update_data(self):
        """Fetch data and back off while the meter is offline."""
        try:
            data = await self.my_api.async_refresh_modbus_data()
        except (OSError, TimeoutError, ModbusException, ValueError, IndexError) as err:
            self._consecutive_failures = min(self._consecutive_failures + 1, 5)
            retry_interval = min(
                OFFLINE_RETRY_INTERVAL * 2 ** (self._consecutive_failures - 1),
                MAX_OFFLINE_RETRY_INTERVAL,
            )
            self.update_interval = timedelta(seconds=retry_interval)
            self.my_api.close()
            raise UpdateFailed(
                f"Error communicating with meter: {err}"
            ) from err

        self._consecutive_failures = 0
        self.update_interval = self._normal_update_interval
        return data

    async def async_shutdown(self):
        """Stop scheduled updates and close the Modbus connection."""
        await super().async_shutdown()
        self.my_api.close()


class IammeterModbusHub:
    """Asynchronous wrapper for pymodbus."""

    def __init__(
        self,
        name,
        host,
        port,
        type,
    ):
        """Initialize the Modbus hub."""
        self._client = AsyncModbusTcpClient(
            host=host,
            port=int(port),
            timeout=2,
            retries=0,
            reconnect_delay=0,
        )
        self._value_attr_name = "count"
        self._name = name
        self._type = type
        self.data = {}

    async def async_refresh_modbus_data(self):
        """Connect if needed and perform one asynchronous Modbus read."""
        if not self._client.connected and not await self._client.connect():
            raise ConnectionException("Unable to connect to meter")

        await self.read_modbus_holding_registers()
        return self.data

    @property
    def name(self):
        """Return the name of this hub."""
        return self._name

    def close(self):
        """Disconnect client."""
        self._client.close()

    async def read_modbus_holding_registers(self):
        """Read modbus holding registers with error handling and modern API."""
        typeCount = 66  # Extended to include all registers up to runtime at 64-65
        if self._type == TYPE_3080:
            typeCount = 8

        try:
            # pymodbus < 3.10.0. Try this first because older releases accept
            # and silently ignore unknown keyword arguments.
            resp = await self._client.read_holding_registers(
                address=0x0,
                count=typeCount,
                slave=1,
            )
        except TypeError:
            # pymodbus >= 3.10.0
            resp = await self._client.read_holding_registers(
                address=0x0,
                count=typeCount,
                device_id=1,
            )

        if resp.isError():
            raise ModbusException(f"Modbus read error: {resp}")

        regs = resp.registers
        if len(regs) < typeCount:
            raise ModbusException(
                f"Short Modbus response: expected {typeCount} registers, got {len(regs)}"
            )

        def u16(i):
            """Read 16-bit unsigned integer"""
            return regs[i] & 0xFFFF

        def s32(i):
            """Read 32-bit signed integer"""
            value = (regs[i] << 16) | regs[i + 1]
            return value - 0x100000000 if value & 0x80000000 else value

        def u32(i):
            """Read 32-bit unsigned integer"""
            return (regs[i] << 16) | regs[i + 1]

        if self._type == TYPE_3080:
            voltage_a = u16(0)
            self.data["voltage_a"] = round(voltage_a * 0.01, 1)

            current_a = u16(1)
            self.data["current_a"] = round(current_a * 0.01, 1)

            power_a = s32(2)                # 2~3
            self.data["power_a"] = power_a

            import_energy_a = u32(4)        # 4~5
            self.data["import_energy_a"] = round(
                import_energy_a * 0.0003125, 3)

            export_energy_a = u32(6)        # 6~7
            self.data["export_energy_a"] = round(
                export_energy_a * 0.0003125, 3)
            return True
        else:
            voltage_a = u16(0)
            self.data["voltage_a"] = round(voltage_a * 0.01, 1)

            current_a = u16(1)
            self.data["current_a"] = round(current_a * 0.01, 1)

            power_a = s32(2)                    # 2~3
            self.data["power_a"] = power_a

            import_energy_a = u32(4)            # 4~5
            self.data["import_energy_a"] = round(import_energy_a * 0.00125, 2)

            export_energy_a = u32(6)            # 6~7
            self.data["export_energy_a"] = round(export_energy_a * 0.00125, 2)

            power_factor_a = u16(8)             # 8
            self.data["power_factor_a"] = round(power_factor_a * 0.001, 2)

            # Skip register 9
            voltage_b = u16(10)
            self.data["voltage_b"] = round(voltage_b * 0.01, 1)

            current_b = u16(11)
            self.data["current_b"] = round(current_b * 0.01, 1)

            power_b = s32(12)                   # 12~13
            self.data["power_b"] = power_b

            import_energy_b = u32(14)           # 14~15
            self.data["import_energy_b"] = round(import_energy_b * 0.00125, 2)

            export_energy_b = u32(16)           # 16~17
            self.data["export_energy_b"] = round(export_energy_b * 0.00125, 2)

            power_factor_b = u16(18)            # 18
            self.data["power_factor_b"] = round(power_factor_b * 0.001, 2)

            if self._type != TYPE_2067:
                # Skip register 19
                voltage_c = u16(20)
                self.data["voltage_c"] = round(voltage_c * 0.01, 1)

                current_c = u16(21)
                self.data["current_c"] = round(current_c * 0.01, 1)

                power_c = s32(22)                   # 22~23
                self.data["power_c"] = power_c

                import_energy_c = u32(24)           # 24~25
                self.data["import_energy_c"] = round(
                    import_energy_c * 0.00125, 2
                )

                export_energy_c = u32(26)           # 26~27
                self.data["export_energy_c"] = round(
                    export_energy_c * 0.00125, 2
                )

                power_factor_c = u16(28)            # 28
                self.data["power_factor_c"] = round(power_factor_c * 0.001, 2)

            # Skip register 29
            frequency = u16(30)
            self.data["frequency"] = round(frequency * 0.01, 1)

            # Skip register 31
            total_power = s32(32)               # 32~33
            self.data["total_power"] = total_power

            total_import_energy = u32(34)       # 34~35
            self.data["total_import_energy"] = round(
                total_import_energy * 0.00125, 2)

            total_export_energy = u32(36)       # 36~37
            self.data["total_export_energy"] = round(
                total_export_energy * 0.00125, 2)

            # Reactive power readings
            reactive_power_a = s32(38)           # 38~39
            self.data["reactive_power_a"] = reactive_power_a

            inductive_kvarh_a = u32(40)          # 40~41
            self.data["inductive_kvarh_a"] = round(inductive_kvarh_a / 1000, 3)

            capacitive_kvarh_a = u32(42)         # 42~43
            self.data["capacitive_kvarh_a"] = round(capacitive_kvarh_a / 1000, 3)

            reactive_power_b = s32(44)           # 44~45
            self.data["reactive_power_b"] = reactive_power_b

            inductive_kvarh_b = u32(46)          # 46~47
            self.data["inductive_kvarh_b"] = round(inductive_kvarh_b / 1000, 3)

            capacitive_kvarh_b = u32(48)         # 48~49
            self.data["capacitive_kvarh_b"] = round(capacitive_kvarh_b / 1000, 3)

            if self._type != TYPE_2067:
                reactive_power_c = s32(50)           # 50~51
                self.data["reactive_power_c"] = reactive_power_c

                inductive_kvarh_c = u32(52)          # 52~53
                self.data["inductive_kvarh_c"] = round(
                    inductive_kvarh_c / 1000, 3
                )

                capacitive_kvarh_c = u32(54)         # 54~55
                self.data["capacitive_kvarh_c"] = round(
                    capacitive_kvarh_c / 1000, 3
                )

            # Runtime at address 64
            runtime = u32(64)                    # 64~65
            self.data["runtime"] = runtime

            return True
