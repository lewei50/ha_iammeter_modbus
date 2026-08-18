"""Model-specific IAMMETER Modbus TCP value conversion."""

HIGH_RESOLUTION_MODELS = frozenset({"WEM3046T", "WEM3063T"})


def decode_current(raw_value: int, meter_type: str) -> float:
    """Decode a phase current register to amperes."""
    divisor = 1000 if meter_type in HIGH_RESOLUTION_MODELS else 100
    precision = 3 if divisor == 1000 else 2
    return round(raw_value / divisor, precision)


def decode_power(raw_value: int, meter_type: str) -> int | float:
    """Decode signed active or reactive power to W/var."""
    if meter_type in HIGH_RESOLUTION_MODELS:
        return round(raw_value / 10, 1)
    return raw_value
