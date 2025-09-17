from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfReactivePower,
	UnitOfReactiveEnergy,
    UnitOfTime,
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
    	native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"current_a": IamMeterModbusSensorEntityDescription(
		name="Current A",
		key="current_a",
		native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"power_a": IamMeterModbusSensorEntityDescription(
    	name="Power A",
    	key="power_a",
    	native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"import_energy_a": IamMeterModbusSensorEntityDescription(
		name="Import Energy A",
		key="import_energy_a",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"export_energy_a": IamMeterModbusSensorEntityDescription(
		name="Export Energy A",
		key="export_energy_a",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"power_factor_a": IamMeterModbusSensorEntityDescription(
		name="Power Factor A",
		key="power_factor_a",
    	native_unit_of_measurement=None,
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"voltage_b": IamMeterModbusSensorEntityDescription(
    	name="Voltage B",
    	key="voltage_b",
    	native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"current_b": IamMeterModbusSensorEntityDescription(
		name="Current B",
		key="current_b",
		native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"power_b": IamMeterModbusSensorEntityDescription(
    	name="Power B",
    	key="power_b",
    	native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"import_energy_b": IamMeterModbusSensorEntityDescription(
		name="Import Energy B",
		key="import_energy_b",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"export_energy_b": IamMeterModbusSensorEntityDescription(
		name="Export Energy B",
		key="export_energy_b",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"power_factor_b": IamMeterModbusSensorEntityDescription(
		name="Power Factor B",
		key="power_factor_b",
    	native_unit_of_measurement=None,
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
	),

	"voltage_c": IamMeterModbusSensorEntityDescription(
    	name="Voltage C",
    	key="voltage_c",
    	native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"current_c": IamMeterModbusSensorEntityDescription(
		name="Current C",
		key="current_c",
		native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"power_c": IamMeterModbusSensorEntityDescription(
    	name="Power C",
    	key="power_c",
    	native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"import_energy_c": IamMeterModbusSensorEntityDescription(
		name="Import Energy C",
		key="import_energy_c",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"export_energy_c": IamMeterModbusSensorEntityDescription(
		name="Export Energy C",
		key="export_energy_c",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"power_factor_c": IamMeterModbusSensorEntityDescription(
		name="Power Factor C",
		key="power_factor_c",
    	native_unit_of_measurement=None,
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"frequency": IamMeterModbusSensorEntityDescription(
    	name="Frequency",
    	key="frequency",
    	native_unit_of_measurement=UnitOfFrequency.HERTZ,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
    ),
	"total_power": IamMeterModbusSensorEntityDescription(
    	name="Total Power",
    	key="total_power",
    	native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"total_import_energy": IamMeterModbusSensorEntityDescription(
		name="Total Import Energy",
		key="total_import_energy",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"total_export_energy": IamMeterModbusSensorEntityDescription(
		name="Total Export Energy",
		key="total_export_energy",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"reactive_power_a": IamMeterModbusSensorEntityDescription(
		name="Reactive Power A",
		key="reactive_power_a",
		native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"reactive_power_b": IamMeterModbusSensorEntityDescription(
		name="Reactive Power B",
		key="reactive_power_b",
		native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"reactive_power_c": IamMeterModbusSensorEntityDescription(
		name="Reactive Power C",
		key="reactive_power_c",
		native_unit_of_measurement=UnitOfReactivePower.VOLT_AMPERE_REACTIVE,
        device_class=SensorDeviceClass.REACTIVE_POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"inductive_kvarh_a": IamMeterModbusSensorEntityDescription(
		name="Inductive KVARH A",
		key="inductive_kvarh_a",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"capacitive_kvarh_a": IamMeterModbusSensorEntityDescription(
		name="Capacitive KVARH A",
		key="capacitive_kvarh_a",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"inductive_kvarh_b": IamMeterModbusSensorEntityDescription(
		name="Inductive KVARH B",
		key="inductive_kvarh_b",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"capacitive_kvarh_b": IamMeterModbusSensorEntityDescription(
		name="Capacitive KVARH B",
		key="capacitive_kvarh_b",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"inductive_kvarh_c": IamMeterModbusSensorEntityDescription(
		name="Inductive KVARH C",
		key="inductive_kvarh_c",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"capacitive_kvarh_c": IamMeterModbusSensorEntityDescription(
		name="Capacitive KVARH C",
		key="capacitive_kvarh_c",
		native_unit_of_measurement=UnitOfReactiveEnergy.KILO_VOLT_AMPERE_REACTIVE_HOUR,
        device_class=SensorDeviceClass.REACTIVE_ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"runtime": IamMeterModbusSensorEntityDescription(
		name="Runtime",
		key="runtime",
		native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
}

SENSOR_TYPES_3080: dict[str, list[IamMeterModbusSensorEntityDescription]] = {
    "voltage_a": IamMeterModbusSensorEntityDescription(
    	name="Voltage",
    	key="voltage_a",
    	native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"current_a": IamMeterModbusSensorEntityDescription(
		name="Current",
		key="current_a",
		native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
	),
	"power_a": IamMeterModbusSensorEntityDescription(
    	name="Power",
    	key="power_a",
    	native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	"import_energy_a": IamMeterModbusSensorEntityDescription(
		name="Import Energy",
		key="import_energy_a",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
	"export_energy_a": IamMeterModbusSensorEntityDescription(
		name="Export Energy",
		key="export_energy_a",
		native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
}
