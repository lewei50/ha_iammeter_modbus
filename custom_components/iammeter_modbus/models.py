"""IAMMETER model detection helpers."""

MODEL_ID_TO_TYPE = {
    1: "WEM3080",
    2: "WEM3080T",
    3: "WEM3046T",
    4: "WEM3050T",
    5: "WEM2067",
    6: "WEM3063T",
}


def detect_meter_type(model_id):
    """Return the meter type for a Modbus TCP model register value."""
    try:
        return MODEL_ID_TO_TYPE[model_id]
    except KeyError as err:
        raise ValueError(f"Unsupported IAMMETER model ID: {model_id}") from err
