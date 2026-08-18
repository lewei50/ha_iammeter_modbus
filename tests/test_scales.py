import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "iammeter_modbus"
    / "scales.py"
)
SPEC = importlib.util.spec_from_file_location("iammeter_modbus_scales", MODULE_PATH)
scales = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scales)


class ModelScaleTests(unittest.TestCase):
    def test_wem3046t_and_wem3063t_high_resolution_scales(self):
        for meter_type in ("WEM3046T", "WEM3063T"):
            self.assertEqual(scales.decode_current(1234, meter_type), 1.234)
            self.assertEqual(scales.decode_power(1180, meter_type), 118.0)
            self.assertEqual(scales.decode_power(-1180, meter_type), -118.0)

    def test_other_three_phase_models_keep_generic_scales(self):
        for meter_type in ("WEM3080T", "WEM3050T"):
            self.assertEqual(scales.decode_current(1234, meter_type), 12.34)
            self.assertEqual(scales.decode_power(1180, meter_type), 1180)


if __name__ == "__main__":
    unittest.main()
