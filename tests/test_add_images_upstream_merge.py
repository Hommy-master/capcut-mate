import json
import unittest

from src.service.add_images import parse_image_data


class AddImagesUpstreamMergeTests(unittest.TestCase):
    def _image(self, **overrides):
        image = {
            "image_url": "https://example.com/image.png",
            "start": 0,
            "end": 2_000_000,
            "transition": "\u53e0\u5316",
            "ken_burns": {
                "start_scale": 1.0,
                "end_scale": 1.06,
                "start_x": 0,
                "end_x": 0.03,
            },
        }
        image.update(overrides)
        return image

    def test_missing_transition_duration_uses_default_and_keeps_ken_burns(self):
        parsed = parse_image_data(json.dumps([self._image()]))[0]

        self.assertIsNone(parsed["transition_duration"])
        self.assertEqual(1.06, parsed["ken_burns"]["end_scale"])

    def test_empty_transition_duration_uses_default(self):
        parsed = parse_image_data(
            json.dumps([self._image(transition_duration="")])
        )[0]

        self.assertIsNone(parsed["transition_duration"])

    def test_explicit_transition_duration_is_preserved(self):
        parsed = parse_image_data(
            json.dumps([self._image(transition_duration=750_000)])
        )[0]

        self.assertEqual(750_000, parsed["transition_duration"])


if __name__ == "__main__":
    unittest.main()
