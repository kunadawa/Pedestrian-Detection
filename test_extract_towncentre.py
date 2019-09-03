import unittest
from extract_towncentre import validate_video_path
import tempfile

class TestExtractTownCentre(unittest.TestCase):
    def test_validate_video_path_invalid(self):
        file = "/tmp/xyz"
        result = validate_video_path("/tmp/xyz")
        self.assertIsNotNone(result, "validation should not produce a None result")
        status, msg = result
        self.assertFalse(status, "validation should fail for an non-existent path")
        self.assertEqual(msg, f"{file} does not exist")

    def test_validate_video_path_valid(self):
        file = tempfile.NamedTemporaryFile(suffix=".vid")
        result = validate_video_path(file.name)
        self.assertIsNotNone(result, "validation should not produce a None result")
        status, msg = result
        self.assertTrue(status, f"validation should succeed for valid path {file.name}")
        self.assertEqual(msg, f"Processing {file.name}...")
        file.close()

if __name__ == '__main__':
    unittest.main()
