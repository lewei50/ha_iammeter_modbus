import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "iammeter_modbus"
    / "models.py"
)
SPEC = importlib.util.spec_from_file_location("iammeter_models", MODULE_PATH)
MODELS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODELS)


class MeterModelDetectionTest(unittest.TestCase):
    def test_all_supported_model_ids(self):
        self.assertEqual(
            {
                model_id: MODELS.detect_meter_type(model_id)
                for model_id in range(1, 7)
            },
            {
                1: "WEM3080",
                2: "WEM3080T",
                3: "WEM3046T",
                4: "WEM3050T",
                5: "WEM2067",
                6: "WEM3063T",
            },
        )

    def test_unknown_model_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported IAMMETER model ID: 0"):
            MODELS.detect_meter_type(0)


if __name__ == "__main__":
    unittest.main()
