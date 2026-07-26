import json
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

from src.pyJianYingDraft.keyframe import KeyframeProperty
from src.service.add_images import add_image_to_draft, parse_image_data


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
        self.assertIsInstance(parsed["transition_duration"], int)

    def test_add_image_applies_ken_burns_and_default_transition_duration(self):
        script = MagicMock(width=1920, height=1080)
        segment = MagicMock()
        segment.segment_id = "segment-1"
        segment.material_instance.material_id = "material-1"
        image = self._image(
            local_image_path=None,
            ken_burns={
                "start_scale": 1.0,
                "end_scale": 1.06,
                "start_x": 0,
                "end_x": 0.03,
                "start_y": 0,
                "end_y": -0.02,
            },
        )

        with tempfile.NamedTemporaryFile() as image_file, patch(
            "src.service.add_images.draft.VideoSegment", return_value=segment
        ):
            image["local_image_path"] = image_file.name
            segment_id, segment_info = add_image_to_draft(
                script,
                "images",
                image_file.name,
                image,
            )

        self.assertEqual("segment-1", segment_id)
        self.assertEqual(2_000_000, segment_info.end)
        self.assertEqual(
            [
                call(KeyframeProperty.uniform_scale, 0, 1.0),
                call(KeyframeProperty.uniform_scale, 2_000_000, 1.06),
                call(KeyframeProperty.position_x, 0, 0.0),
                call(KeyframeProperty.position_x, 2_000_000, 0.03),
                call(KeyframeProperty.position_y, 0, 0.0),
                call(KeyframeProperty.position_y, 2_000_000, -0.02),
            ],
            segment.add_keyframe.call_args_list,
        )
        segment.add_transition.assert_called_once()
        self.assertIsNone(segment.add_transition.call_args.kwargs["duration"])
        script.add_segment.assert_called_once_with(segment, "images")

    def test_add_image_casts_explicit_transition_duration_to_int(self):
        script = MagicMock(width=1920, height=1080)
        segment = MagicMock()
        segment.segment_id = "segment-1"
        segment.material_instance.material_id = "material-1"
        image = self._image(
            local_image_path=None,
            transition_duration="750000",
            ken_burns=None,
        )

        with tempfile.NamedTemporaryFile() as image_file, patch(
            "src.service.add_images.draft.VideoSegment", return_value=segment
        ):
            image["local_image_path"] = image_file.name
            add_image_to_draft(script, "images", image_file.name, image)

        duration = segment.add_transition.call_args.kwargs["duration"]
        self.assertEqual(750_000, duration)
        self.assertIsInstance(duration, int)


if __name__ == "__main__":
    unittest.main()
