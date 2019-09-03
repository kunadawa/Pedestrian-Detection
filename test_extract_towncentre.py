import unittest
from extract_towncentre import validate_video_path, process_video_cmd_args
import tempfile
from unittest.mock import Mock

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

    def test_process_video_cmd_args_no_cmd_args(self):
        extract_mock = Mock()
        # when no args are passed, only the script name is present
        argv = ['script/path']
        process_video_cmd_args(argv, extract_mock.validate_video_path, extract_mock.video2im,)
        extract_mock.video2im.assert_called_once()
        extract_mock.validate_video_path.assert_not_called()

    def test_process_video_cmd_args_with_invalid_cmd_args(self):
        extract_mock = Mock()
        mock_path = 'video-file'
        extract_mock.validate_video_path = Mock(return_value=(False, f"Bad {mock_path}"))
        argv = ['script/path', mock_path]
        process_video_cmd_args(argv, extract_mock.validate_video_path, extract_mock.video2im,)
        extract_mock.video2im.assert_not_called()
        extract_mock.validate_video_path.assert_called_once_with(mock_path)

    def test_process_video_cmd_args_with_valid_cmd_args(self):
        extract_mock = Mock()
        mock_path = 'video-file'
        extract_mock.validate_video_path = Mock(return_value=(True, f"Good {mock_path}"))
        argv = ['script/path', mock_path]
        process_video_cmd_args(argv, extract_mock.validate_video_path, extract_mock.video2im,)
        extract_mock.video2im.assert_called_once_with(src=mock_path)
        extract_mock.validate_video_path.assert_called_once_with(mock_path)


if __name__ == '__main__':
    unittest.main()
