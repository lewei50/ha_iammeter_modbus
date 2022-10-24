from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntityDescription,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

from homeassistant.const import (
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_CURRENT_MILLIAMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_VOLT_AMPERE,
    POWER_WATT,
)

TYPE_3080 = "WEM3080"
TYPE_3080T = "WEM3080T"

DOMAIN = "iammeter_modbus"
DEFAULT_NAME = "IamMeter"
DEFAULT_SCAN_INTERVAL = 2
DEFAULT_PORT = 502
DEFAULT_TYPE = TYPE_3080T
CONF_IamMeter_HUB = "iammeter_hub"
ATTR_MANUFACTURER = "IamMeter"

@dataclass
class IamMeterModbusSensorEntityDescription(SensorEntityDescription):
    """A class that describes IamMeter Modbus sensor entities."""

SENSOR_TYPES: dict[str, list[IamMeterModbusSensorEntityDescription]] = {
    "voltage_a": IamMeterModbusSensorEntityDescription(
    	name="Voltage A",
    	key="voltage_a",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"current_a": IamMeterModbusSensorEntityDescription(
		name="Current A",
		key="current_a",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
	),
	"power_a": IamMeterModbusSensorEntityDescription(
    	name="Power A",
    	key="power_a",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"import_energy_a": IamMeterModbusSensorEntityDescription(
		name="Import Energy A",
		key="import_energy_a",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"export_energy_a": IamMeterModbusSensorEntityDescription(
		name="Export Energy A",
		key="export_energy_a",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"power_factor_a": IamMeterModbusSensorEntityDescription(
		name="Power Factor A",
		key="power_factor_a",
		
        device_class=DEVICE_CLASS_POWER_FACTOR,
	),
	"voltage_b": IamMeterModbusSensorEntityDescription(
    	name="Voltage B",
    	key="voltage_b",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"current_b": IamMeterModbusSensorEntityDescription(
		name="Current B",
		key="current_b",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
	),
	"power_b": IamMeterModbusSensorEntityDescription(
    	name="Power B",
    	key="power_b",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"import_energy_b": IamMeterModbusSensorEntityDescription(
		name="Import Energy B",
		key="import_energy_b",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"export_energy_b": IamMeterModbusSensorEntityDescription(
		name="Export Energy B",
		key="export_energy_b",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"power_factor_b": IamMeterModbusSensorEntityDescription(
		name="Power Factor B",
		key="power_factor_b",
		
        device_class=DEVICE_CLASS_POWER_FACTOR,
	),

	"voltage_c": IamMeterModbusSensorEntityDescription(
    	name="Voltage C",
    	key="voltage_c",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"current_c": IamMeterModbusSensorEntityDescription(
		name="Current C",
		key="current_c",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
	),
	"power_c": IamMeterModbusSensorEntityDescription(
    	name="Power C",
    	key="power_c",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"import_energy_c": IamMeterModbusSensorEntityDescription(
		name="Import Energy C",
		key="import_energy_c",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"export_energy_c": IamMeterModbusSensorEntityDescription(
		name="Export Energy C",
		key="export_energy_c",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"power_factor_c": IamMeterModbusSensorEntityDescription(
		name="Power Factor C",
		key="power_factor_c",
		
        device_class=DEVICE_CLASS_POWER_FACTOR,
	),
	"frequency": IamMeterModbusSensorEntityDescription(
    	name="Frequency",
    	key="frequency",
    	native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
	"total_power": IamMeterModbusSensorEntityDescription(
    	name="Total Power",
    	key="total_power",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"total_import_energy": IamMeterModbusSensorEntityDescription(
		name="Total Import Energy",
		key="total_import_energy",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"total_export_energy": IamMeterModbusSensorEntityDescription(
		name="Total Export Energy",
		key="total_export_energy",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
}

SENSOR_TYPES_3080: dict[str, list[IamMeterModbusSensorEntityDescription]] = {
    "voltage_a": IamMeterModbusSensorEntityDescription(
    	name="Voltage",
    	key="voltage_a",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"current_a": IamMeterModbusSensorEntityDescription(
		name="Current",
		key="current_a",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
	),
	"power_a": IamMeterModbusSensorEntityDescription(
    	name="Power",
    	key="power_a",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"import_energy_a": IamMeterModbusSensorEntityDescription(
		name="Import Energy",
		key="import_energy_a",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"export_energy_a": IamMeterModbusSensorEntityDescription(
		name="Export Energy",
		key="export_energy_a",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
}
