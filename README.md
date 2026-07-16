[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

This project is forked from [wills106](https://github.com/wills106/homeassistant-iammeter-modbus).
It adds single-phase meter support and device auto-discovery.

# Home Assistant IAMMETER Modbus TCP
IAMMETER Modbus TCP custom component for Home Assistant.

Requires firmware version 75.82 or later.

Multiple instances are supported. Give each meter a unique name, such as
`IAMMETER Main` or `IAMMETER Garage`.

Supports:

- WEM3080
- WEM3080T
- WEM3050T
- WEM3046T
- WEM2067

# IAMMETER

------

[IAMMETER](https://www.iammeter.com/) meters supported by this integration include
the single-phase WEM3080, three-phase WEM3080T/WEM3050T/WEM3046T, and split-meter
WEM2067 models.

## Installation

------

### Manual Installation

1. Copy `iammeter_modbus` folder into your custom_components folder in your hass configuration directory.
2. Restart Home Assistant.

### Installation with HACS (Home Assistant Community Store)

1. Ensure that HACS is installed.
2. In HACS / Integrations /explore&download repositories/iammeter, add the url the this repository.
3. Search for and install the `iammeter` integration.
4. Restart Home Assistant.

## Configuration

It is configurable through config flow, meaning it will popup a dialog after adding the integration.

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for `iammeter_modbus`.
3. Enter a unique name for the meter.
4. Enter the meter IP address, device type and Modbus TCP port (default: `502`).
5. Set the polling interval in seconds (default: `3`, allowed range: `1–3600`).
6. Select **Submit → Finish**.

For an existing device, select **Reconfigure** on the integration entry to update
its IP address, Modbus TCP port, or polling interval. Saving these settings
reloads the integration automatically. The device name and model cannot be
changed from this page.

The configured polling interval is used while the meter is online. If the meter
goes offline, retries automatically back off to 5, 10, 20, 40 and then 60
seconds, avoiding excessive connection attempts. The configured polling interval
is restored automatically when the meter comes back online.

## Sensors

Sensors available in the library:

### SINGLE-PHASE ENERGY METER (WEM3080/WEM3162)

| name                 | Unit | Description                  |
| :------------------- | :--- | :--------------------------- |
| wem3080_voltage      | V    | Voltage.                     |
| wem3080_current      | A    | current.                     |
| wem3080_power        | W    | active power.                |
| wem3080_importenergy | kWh  | Energy consumption from grid |
| wem3080_exportgrid   | kWh  | Energy export to grid        |

### THREE-PHASE ENERGY METER (WEM3080T/WEM3050T/WEM3046T)

| name                    | Unit | Description           |
| :---------------------- | :--- | :-------------------- |
| wem3080t_voltage_a      | V    | A phase voltage       |
| wem3080t_current_a      | A    | A phase current       |
| wem3080t_power_a        | W    | A phase active power  |
| wem3080t_importenergy_a | kWh  | A phase import energy |
| wem3080t_exportgrid_a   | kWh  | A phase export energy |
| wem3080t_frequency      | Hz   | Frequency             |
| wem3080t_pf_a           |      | A phase power factor  |
|                         |      |                       |
| wem3080t_voltage_b      | V    | B phase voltage       |
| wem3080t_current_b      | A    | B phase current       |
| wem3080t_power_b        | W    | B phase active power  |
| wem3080t_importenergy_b | kWh  | B phase import energy |
| wem3080t_exportgrid_b   | kWh  | B phase export energy |
| wem3080t_pf_b           |      | B phase power factor  |
|                         |      |                       |
| wem3080t_voltage_c      | V    | C phase voltage       |
| wem3080t_current_c      | A    | C phase current       |
| wem3080t_power_c        | W    | C phase active power  |
| wem3080t_importenergy_c | kWh  | C phase import energy |
| wem3080t_exportgrid_c   | kWh  | C phase export energy |
| wem3080t_pf_c           |      | C phase power factor  |
|                         |      |                       |
| wem3080t_total_power    | W    | Total active power    |
| wem3080t_total_import_energy | kWh | Total import energy |
| wem3080t_total_export_energy | kWh | Total export energy |
| wem3080t_reactive_power_a | var | A phase reactive power |
| wem3080t_inductive_kvarh_a | kvarh | A phase inductive reactive energy |
| wem3080t_capacitive_kvarh_a | kvarh | A phase capacitive reactive energy |
| wem3080t_reactive_power_b | var | B phase reactive power |
| wem3080t_inductive_kvarh_b | kvarh | B phase inductive reactive energy |
| wem3080t_capacitive_kvarh_b | kvarh | B phase capacitive reactive energy |
| wem3080t_reactive_power_c | var | C phase reactive power |
| wem3080t_inductive_kvarh_c | kvarh | C phase inductive reactive energy |
| wem3080t_capacitive_kvarh_c | kvarh | C phase capacitive reactive energy |
| wem3080t_runtime        | s    | Meter runtime          |

### SPLIT METER (WEM2067)

WEM2067 provides the same A-phase, B-phase, frequency, total, reactive-energy,
and runtime sensors listed above. C-phase sensors are not created for this model.
